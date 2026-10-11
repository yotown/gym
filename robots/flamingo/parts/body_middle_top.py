"""Flamingo body middle (the top half): the Duck's own, with each wing mount's two screws and its servo's
cable through the side wall, and four standoffs under its ceiling for the Pi (moved from the Duck's head).
Not in the model: the Pi's screws.

Frame: the Duck's (body_middle_top's): x forward, y left, z up.
"""

import runpy

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)
DUCK = runpy.run_path(S.duck("body_middle_top"))

# -- interfaces -- fixed: the wing mounts' (shared.py) ------------------------------------------------
HOLE_D = S.CLEARANCE["M3"].hole_d
c0, c1, ch = S.CABLE_WINDOW

shell = DUCK["result"]
for side, d in (("left", 1), ("right", -1)):
    y = d * (S.WALL_Y + 1)              # from just outside the wall, inwards through it
    wall = cq.Workplane(cq.Plane(origin=(0, y, 0), xDir=(1, 0, 0), normal=(0, -d, 0)))
    for into, across in S.BASE_SCREWS:
        x, _, z = S.to_body(side, (S.FAR, across, into))
        shell = shell.cut(wall.center(x, z).circle(HOLE_D / 2).extrude(S.WALL_T + 2))
    xs = [S.to_body(side, (S.FAR, 0.0, z))[0] for z in (c0, c1)]
    zc = S.to_body(side, (S.FAR, 0.0, 0.0))[2]
    shell = shell.cut(wall.center(sum(xs) / 2, zc).rect(abs(xs[1] - xs[0]), 2 * ch).extrude(S.WALL_T + 2))

# the Pi's standoffs, down from the ceiling (shared.py: where it hangs)
pts, drop = S.pi_holes(), S.PI_STANDOFF
shell = shell.union(cq.Workplane("XY", origin=(0, 0, S.CEILING_Z + 0.5)).pushPoints(pts).circle(S.STANDOFF_D / 2).extrude(-(drop + 0.5)))
shell = shell.cut(cq.Workplane("XY", origin=(0, 0, S.CEILING_Z - drop - 1)).pushPoints(pts).circle(S.PI_HOLE_D / 2).extrude(drop + 1))
result = shell
