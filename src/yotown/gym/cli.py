"""gym: build, check and compare a robot's parts.

    gym build so101 [--out build/so101] [--step] [--stl]   # every part, as STEP and STL
    gym check so101                                        # every part builds one valid solid
    gym diff so101 [REV]                                   # what each part gains and loses since REV (default HEAD)

A robot is robots/<robot>/: its parts (parts/<part>.py, each ending in `result`) and what they share
(shared.py). Run it from the repository, or give the path with --robots. Each part is built in its
own process, so a crash in one part does not affect the others.
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor

TOL_MM3 = 1e-3          # a part whose gain and loss are both under this is unchanged


# ── finding a robot's parts ──────────────────────────────────────────────────

def robots_dir(given: str | None) -> str:
    """robots/ from --robots, or the nearest one at or above the working directory."""
    if given:
        return os.path.abspath(given)
    d = os.getcwd()
    while True:
        if os.path.isdir(os.path.join(d, "robots")):
            return os.path.join(d, "robots")
        if os.path.dirname(d) == d:
            raise SystemExit("no robots/ here or above; pass --robots")
        d = os.path.dirname(d)


def parts_of(robot_dir: str) -> dict:
    """{part: program} for robots/<robot>/parts/*.py."""
    folder = os.path.join(robot_dir, "parts")
    if not os.path.isdir(folder):
        raise SystemExit("%s has no parts/" % robot_dir)
    return {f[:-3]: os.path.join(folder, f) for f in sorted(os.listdir(folder))
            if f.endswith(".py") and not f.startswith("_")}


# ── building, one part per process ───────────────────────────────────────────

def _solid(program: str):
    import runpy
    import xml.etree.ElementTree  # noqa: F401 -- loaded before cadquery, as some parts need
    import cadquery as cq
    r = runpy.run_path(program, run_name="__main__")["result"]
    return r.val() if isinstance(r, cq.Workplane) else r


def _summary(shape) -> dict:
    bb = shape.BoundingBox()
    return {"solids": len(shape.Solids()), "valid": bool(shape.isValid()), "volume_mm3": round(shape.Volume(), 3),
            "box_mm": [round(v, 3) for v in (bb.xmin, bb.ymin, bb.zmin, bb.xmax, bb.ymax, bb.zmax)]}


def _build(job: tuple) -> dict:
    name, program, out, step, stl = job
    try:
        shape = _solid(program)
        row = {"part": name, "ok": True, **_summary(shape)}
        row["ok"] = row["solids"] == 1 and row["valid"]
        if out:
            import cadquery as cq
            if step:
                cq.exporters.export(shape, os.path.join(out, name + ".step"))
            if stl:
                cq.exporters.export(shape, os.path.join(out, name + ".stl"), tolerance=0.02, angularTolerance=0.1)
        return row
    except Exception as e:                                  # noqa: BLE001 -- reported, not raised
        return {"part": name, "ok": False, "error": "%s: %s" % (type(e).__name__, str(e).splitlines()[-1] if str(e) else "")}


def _diff(job: tuple) -> dict:
    name, old, new = job
    try:
        if old is None:
            return {"part": name, "change": "added", **_summary(_solid(new))}
        if new is None:
            return {"part": name, "change": "removed"}
        a, b = _solid(old), _solid(new)
        gain, loss = b.cut(a), a.cut(b)
        row = {"part": name, "gain_mm3": round(gain.Volume(), 3), "loss_mm3": round(loss.Volume(), 3),
               "volume_mm3": round(b.Volume(), 3), "volume_was_mm3": round(a.Volume(), 3)}
        changed = row["gain_mm3"] > TOL_MM3 or row["loss_mm3"] > TOL_MM3
        row["change"] = "changed" if changed else "unchanged"
        if changed:
            where = [s for s in (gain, loss) if s.Volume() > TOL_MM3]
            boxes = [s.BoundingBox() for s in where]
            row["where_mm"] = [round(v, 2) for v in (min(x.xmin for x in boxes), min(x.ymin for x in boxes), min(x.zmin for x in boxes),
                                                     max(x.xmax for x in boxes), max(x.ymax for x in boxes), max(x.zmax for x in boxes))]
        return row
    except Exception as e:                                  # noqa: BLE001
        return {"part": name, "change": "error", "error": "%s: %s" % (type(e).__name__, str(e).splitlines()[-1] if str(e) else "")}


def _pool(jobs, fn, workers: int) -> list:
    """Each job in a fresh (spawned) process: a kernel that has run once is not forked."""
    with ProcessPoolExecutor(max_workers=max(1, workers), mp_context=mp.get_context("spawn"), max_tasks_per_child=1) as ex:
        return list(ex.map(fn, jobs))


# ── git: a robot as it was at a revision ─────────────────────────────────────

def robot_at(robot_dir: str, rev: str, into: str) -> str:
    """Write robots/<robot>/ as it was at rev into a folder; return that robot's folder there."""
    top = subprocess.run(["git", "-C", robot_dir, "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if top.returncode:
        raise SystemExit("%s is not in a git repository" % robot_dir)
    top = top.stdout.strip()
    rel = os.path.relpath(robot_dir, top)
    files = subprocess.run(["git", "-C", top, "ls-tree", "-r", "--name-only", rev, "--", rel],
                           capture_output=True, text=True, check=True).stdout.split()
    if not files:
        raise SystemExit("%s has no %s at %s" % (top, rel, rev))
    for f in files:
        dest = os.path.join(into, f)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as out:
            out.write(subprocess.run(["git", "-C", top, "show", "%s:%s" % (rev, f)], capture_output=True, check=True).stdout)
    return os.path.join(into, rel)


# ── the commands ─────────────────────────────────────────────────────────────

def cmd_build(a) -> int:
    robot = os.path.join(robots_dir(a.robots), a.robot)
    parts = parts_of(robot)
    out = os.path.abspath(a.out or os.path.join("build", a.robot)) if (a.step or a.stl) else None
    if out:
        os.makedirs(out, exist_ok=True)
    rows = _pool([(n, p, out, a.step, a.stl) for n, p in parts.items()], _build, a.jobs)
    for r in rows:
        print("%s %-32s %s" % ("ok  " if r["ok"] else "FAIL", r["part"],
                               "%d solid  %.1f mm3" % (r["solids"], r["volume_mm3"]) if "solids" in r else r.get("error", "")))
    bad = sum(not r["ok"] for r in rows)
    print("%s: %d of %d parts build one valid solid%s" % (a.robot, len(rows) - bad, len(rows), "; written to %s" % out if out else ""))
    _json(a, rows)
    return 1 if bad else 0


def cmd_check(a) -> int:
    a.step = a.stl = False
    a.out = None
    return cmd_build(a)


def cmd_diff(a) -> int:
    robot = os.path.join(robots_dir(a.robots), a.robot)
    tmp = tempfile.mkdtemp(prefix="gym_diff_")
    try:
        was = parts_of(robot_at(robot, a.rev, tmp))
        now = parts_of(robot)
        names = sorted(set(was) | set(now))
        rows = _pool([(n, was.get(n), now.get(n)) for n in names], _diff, a.jobs)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for r in rows:
        if r["change"] == "changed":
            print("changed    %-30s +%.3f / -%.3f mm3 (volume %+.4f %%)  at x %.1f..%.1f  y %.1f..%.1f  z %.1f..%.1f" % (
                r["part"], r["gain_mm3"], r["loss_mm3"], 100 * (r["volume_mm3"] / r["volume_was_mm3"] - 1),
                *[r["where_mm"][i] for i in (0, 3, 1, 4, 2, 5)]))
        elif r["change"] != "unchanged" or a.all:
            print("%-10s %-30s %s" % (r["change"], r["part"], r.get("error", "")))
    n = {k: sum(r["change"] == k for r in rows) for k in ("changed", "added", "removed", "error", "unchanged")}
    print("%s since %s: %s" % (a.robot, a.rev, ", ".join("%d %s" % (v, k) for k, v in n.items() if v)))
    _json(a, rows)
    return 1 if n["error"] else 0


def _json(a, rows):
    if getattr(a, "json", ""):
        os.makedirs(os.path.dirname(os.path.abspath(a.json)), exist_ok=True)
        json.dump(rows, open(a.json, "w"), indent=1)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="gym", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--robots", help="the robots/ folder (default: the nearest one at or above here)")
    sub = ap.add_subparsers(dest="command", required=True)

    def common(p):
        p.add_argument("robot")
        p.add_argument("-j", "--jobs", type=int, default=max(1, min(4, (os.cpu_count() or 2) // 2)), help="parts built at once")
        p.add_argument("--json", default="", help="also write the rows as JSON here")
        return p

    b = common(sub.add_parser("build", help="build every part; with --step / --stl, write them"))
    b.add_argument("--out", help="where the files go (default build/<robot>)")
    b.add_argument("--step", action="store_true")
    b.add_argument("--stl", action="store_true")
    b.set_defaults(fn=cmd_build)
    common(sub.add_parser("check", help="every part builds one valid solid")).set_defaults(fn=cmd_check)
    d = common(sub.add_parser("diff", help="what each part gains and loses since a git revision"))
    d.add_argument("rev", nargs="?", default="HEAD")
    d.add_argument("--all", action="store_true", help="list unchanged parts too")
    d.set_defaults(fn=cmd_diff)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
