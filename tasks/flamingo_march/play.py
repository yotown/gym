"""The Flamingo marches: its trained policy driving its MuJoCo model, in plain MuJoCo.

    pip install mujoco onnxruntime numpy
    python tasks/flamingo_march/play.py              # watch it (the MuJoCo viewer, real time)
    python tasks/flamingo_march/play.py --headless   # no window: did it fall, and how closely did it march

flamingo.xml is the model the policy was trained on, in mjlab: the same options, actuators and sensors.
Its printed parts' meshes (meshes/) are built from the part programs in robots/flamingo and
robots/open_duck_mini_v2; bought parts (servos, horns, boards, cells) are boxes of their size.
policy.onnx holds the policy and the march it tracks (one reference pose per control step).

Each control step (task.json: control_dt, decimation) the policy sees the reference's joint angles and
speeds, where the reference's trunk is relative to the robot's, the trunk's IMU, its joints and its last
action; it answers with each joint's target, as an offset from the standing pose.
"""

from __future__ import annotations

import argparse
import json
import os
import time

import mujoco
import numpy as np
import onnxruntime as ort

HERE = os.path.dirname(os.path.abspath(__file__))


def quat_conj(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])


def quat_mul(a, b):
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b
    return np.array([w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2, w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                     w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2, w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2])


def quat_mat(q):
    m = np.zeros(9)
    mujoco.mju_quat2Mat(m, np.asarray(q, dtype=float))
    return m.reshape(3, 3)


class March:
    """The model, the policy, and one control step at a time."""

    def __init__(self, folder: str = HERE):
        self.task = json.load(open(os.path.join(folder, "task.json")))
        self.model = mujoco.MjModel.from_xml_path(os.path.join(folder, self.task["model"]))
        self.data = mujoco.MjData(self.model)
        self.policy = ort.InferenceSession(os.path.join(folder, self.task["policy"]), providers=["CPUExecutionProvider"])
        meta = self.policy.get_modelmeta().custom_metadata_map
        self.joints = meta["joint_names"].split(",")
        self.default = np.array([float(x) for x in meta["default_joint_pos"].split(",")])
        self.scale = np.array([float(x) for x in meta["action_scale"].split(",")])
        bodies = meta["body_names"].split(",")
        self.ref_anchor = bodies.index(meta["anchor_body_name"])
        m = self.model
        self.qadr = np.array([m.joint("robot/" + j).qposadr[0] for j in self.joints])
        self.vadr = np.array([m.joint("robot/" + j).dofadr[0] for j in self.joints])
        by_joint = {m.actuator_trnid[i, 0]: i for i in range(m.nu)}
        self.ctrl = np.array([by_joint[m.joint("robot/" + j).id] for j in self.joints])
        self.anchor = m.body(self.task["anchor_body"]).id
        self.lin_vel = m.sensor(self.task["imu"]["lin_vel"])
        self.ang_vel = m.sensor(self.task["imu"]["ang_vel"])
        self.n_obs = self.policy.get_inputs()[0].shape[1]

    def reference(self, t: int) -> dict:
        """The march at control step t: joint angles and speeds, and each tracked body's pose."""
        names = [o.name for o in self.policy.get_outputs()]
        out = self.policy.run(None, {"obs": np.zeros((1, self.n_obs), np.float32), "time_step": np.array([[t]], np.float32)})
        return {k: v[0] for k, v in zip(names, out)}

    def reset(self):
        """The robot at the march's first pose (its root on the reference's first tracked body)."""
        r = self.reference(0)
        d = self.data
        mujoco.mj_resetData(self.model, d)
        d.qpos[0:3], d.qpos[3:7] = r["body_pos_w"][0], r["body_quat_w"][0]
        d.qvel[0:3] = r["body_lin_vel_w"][0]
        d.qvel[3:6] = quat_mat(r["body_quat_w"][0]).T @ r["body_ang_vel_w"][0]    # the free joint's turn rate is in its own frame
        d.qpos[self.qadr], d.qvel[self.vadr] = r["joint_pos"], r["joint_vel"]
        d.ctrl[self.ctrl] = self.default
        mujoco.mj_forward(self.model, d)
        self.last = np.zeros(len(self.joints))
        self.t = 0

    def observe(self, r: dict) -> np.ndarray:
        d = self.data
        pos, quat = d.xpos[self.anchor], d.xquat[self.anchor]
        ref_pos, ref_quat = r["body_pos_w"][self.ref_anchor], r["body_quat_w"][self.ref_anchor]
        rel_pos = quat_mat(quat).T @ (ref_pos - pos)                     # the reference's trunk, in the robot's trunk frame
        rel_ori = quat_mat(quat_mul(quat_conj(quat), ref_quat))[:, :2].reshape(-1)
        lin = d.sensordata[self.lin_vel.adr[0]:self.lin_vel.adr[0] + 3]
        ang = d.sensordata[self.ang_vel.adr[0]:self.ang_vel.adr[0] + 3]
        return np.concatenate([r["joint_pos"], r["joint_vel"], rel_pos, rel_ori, lin, ang,
                               d.qpos[self.qadr] - self.default, d.qvel[self.vadr], self.last]).astype(np.float32)

    def step(self) -> dict:
        """One control step: observe, act, simulate. The reference it tracked, for the caller to measure against."""
        r = self.reference(self.t)
        obs = self.observe(r)
        action = self.policy.run(["actions"], {"obs": obs[None], "time_step": np.array([[self.t]], np.float32)})[0][0]
        self.data.ctrl[self.ctrl] = self.default + self.scale * action
        for _ in range(self.task["decimation"]):
            mujoco.mj_step(self.model, self.data)
        self.last = action
        self.t += 1
        return r

    def fell(self, r: dict) -> bool:
        """As in training: the trunk 25 cm off the reference's height, or tipped well past it."""
        d = self.data
        if abs(d.xpos[self.anchor][2] - r["body_pos_w"][self.ref_anchor][2]) > 0.25:
            return True
        down = lambda q: quat_mat(q).T @ np.array([0.0, 0.0, -1.0])
        return abs(down(r["body_quat_w"][self.ref_anchor])[2] - down(d.xquat[self.anchor])[2]) > 0.8


def headless(march: March) -> dict:
    march.reset()
    err, steps = [], march.task["steps"] - 1
    for _ in range(steps):
        r = march.step()
        nxt = march.reference(march.t)
        err.append(np.abs(march.data.qpos[march.qadr] - nxt["joint_pos"]).mean())
        if march.fell(nxt):
            return {"fell_at_s": round(march.t * march.task["control_dt"], 2), "steps": march.t}
    return {"fell": False, "seconds": round(steps * march.task["control_dt"], 1),
            "joint_error_rad": round(float(np.mean(err)), 4)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--headless", action="store_true", help="no window: print whether it fell and its mean joint error")
    a = ap.parse_args(argv)
    march = March()
    if a.headless:
        print(json.dumps(headless(march)))
        return 0
    import mujoco.viewer
    with mujoco.viewer.launch_passive(march.model, march.data) as view:
        view.cam.type = mujoco.mjtCamera.mjCAMERA_TRACKING
        view.cam.trackbodyid, view.cam.distance, view.cam.elevation = march.anchor, 1.4, -10
        while view.is_running():
            march.reset()
            for _ in range(march.task["steps"] - 1):
                start = time.time()
                march.step()
                view.sync()
                if not view.is_running():
                    break
                time.sleep(max(0.0, march.task["control_dt"] - (time.time() - start)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
