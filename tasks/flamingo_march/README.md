# The Flamingo marches

The Flamingo (`robots/flamingo`: Open Duck Mini v2 with long legs, wings and a bird's head) marching in
MuJoCo, driven by a trained policy.

```sh
pip install mujoco onnxruntime numpy
python tasks/flamingo_march/play.py              # watch it in the MuJoCo viewer
python tasks/flamingo_march/play.py --headless   # no window: did it fall, and how closely did it march
```

| File | What it is |
|---|---|
| `flamingo.xml` | the model the policy was trained on: masses, joints, actuators, sensors and solver settings |
| `meshes/` | the printed parts' meshes, built from the programs in `robots/flamingo` and `robots/open_duck_mini_v2`, named after them |
| `policy.onnx` | the policy, and the march it tracks: 16 seconds, 50 steps a second |
| `task.json` | the timing and the bodies `play.py` reads |
| `play.py` | the loop: observe, act, simulate |

Bought parts (servos and their horns, boards, cells, the SG90) are boxes of their size here; their masses
are in the model's bodies.

Each step, the policy sees the march's joint angles and speeds at that moment, where the march's trunk is
relative to the robot's, the trunk's IMU (its velocity and turn rate), the robot's joints and its own
last action. It answers with a target angle for each of the 16 joints, as an offset from the standing pose,
and the servos' position control holds it.

`--headless` on our machine: no fall over the 16 seconds, mean joint error 0.095 rad from the march.
(In the simulator it was trained in, from the same start: 0.076 rad.)

The knees work hard. Over the march each knee holds 1.9 N m (RMS), about four times the STS3215's rated
0.49 N m, and reaches the 3.2 N m cap the model sets for each joint (the servo's peak torque). A real Flamingo
would need stronger knee servos or a straighter gait.
