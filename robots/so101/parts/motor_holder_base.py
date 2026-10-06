"""SO-101 base motor holder, written from its STEP: the interfaces exact, the body free.

The wrist holder (motor_holder_wrist) round the back end of the shoulder_pan servo (STS3215): its servo
sits 0.1 mm higher, its boss clears only the -z end (the +z end clears the jaw), and the -z bottom
corner is chamfered at 45 deg instead of rounded (it seats in the base), with a cable clip on the
chamfer and the -z wall's back edge set back.
Frame: the vendor's (Motor_holder_SO101_Base STEP / Menagerie STL, mm), as the wrist holder's: x along
the servo, y up through the plates, z across the walls (the servo's output axis).
"""

import math
import os
import runpy

import cadquery as cq

here = os.path.dirname(os.path.abspath(__file__))
SOURCE = next(p for p in (os.path.join(here, "..", "motor_holder_wrist", "written.py"),
                          os.path.join(here, "motor_holder_wrist.py")) if os.path.exists(p))

# -- interfaces: the held servo, the cradle round it, as the wrist holder's -- fixed ---------------
SERVO_Z = -0.6                             # the servo's origin across the walls (z)

# -- body: free ------------------------------------------------------------------------------------
BOSS_TO = 0.0                              # the boss's room from the -z end to the servo's origin only
SEAT_CHAMFER = 8.0                         # the -z bottom corner, 45 deg
# a cable clip on the chamfer: two bars standing off it, leaning, staggered, the cable between them
CLIP_PROUD, CLIP_BAR_WIDTH, CLIP_GAP, CLIP_R = 3.5, 3.95, 4.4, 0.8   # measured
CLIP_LEAN = 31.2                           # deg from straight across the chamfer, towards -x  # measured
CLIP_AT_X = -45.85                         # the first bar's centre at the floor edge  # measured
CLIP_BARS = [(0.0, 7.8), (2.4, 20.0)]      # each bar from .. to, up its length (the chamfer clips them)  # measured
SETBACK, SETBACK_TOP_Y = 2.35, -26.4       # the -z wall's back edge set back below here, 45 deg above  # measured

holder = runpy.run_path(SOURCE, init_globals={"HOLDER": dict(servo_z=SERVO_Z, seat_chamfer=SEAT_CHAMFER, boss_to=BOSS_TO)})
tube = holder["blank"]                     # the wrist holder before its interfaces are cut
floor_y, half_span, wall, x_from, length = (holder[k] for k in ("FLOOR_Y", "HALF_SPAN", "WALL", "X_FROM", "LENGTH"))

# the cable clip on the seat chamfer: a plane on its face (x as the tube's, y up the chamfer from the floor edge)
chamfer = cq.Plane(origin=(0, floor_y, -half_span + SEAT_CHAMFER), xDir=(1, 0, 0), normal=(0, 1, 1))
up_x, up_y = -math.sin(math.radians(CLIP_LEAN)), math.cos(math.radians(CLIP_LEAN))   # up a bar
pitch = (CLIP_BAR_WIDTH + CLIP_GAP) / up_y                                          # bar to bar, along x
strip = (cq.Workplane(chamfer).center(CLIP_AT_X, SEAT_CHAMFER / 2 ** 0.5)
         .rect(length * 2, SEAT_CHAMFER * 2 ** 0.5).extrude(-CLIP_PROUD))
for i, (s0, s1) in enumerate(CLIP_BARS):
    x0 = CLIP_AT_X + i * pitch
    mid = cq.Location(cq.Vector(x0 + up_x * (s0 + s1) / 2, up_y * (s0 + s1) / 2, 0))
    bar = cq.Sketch().push([mid]).rect(CLIP_BAR_WIDTH, s1 - s0, angle=CLIP_LEAN).reset().vertices().fillet(CLIP_R)
    tube = tube.union(cq.Workplane(chamfer).placeSketch(bar).extrude(-CLIP_PROUD).intersect(strip))

# the -z wall's back edge set back
x1 = x_from + SETBACK
tube = tube.cut(cq.Workplane("XY", origin=(0, 0, -half_span - CLIP_PROUD)).polyline(
    [(x_from - 1, floor_y - CLIP_PROUD), (x1, floor_y - CLIP_PROUD), (x1, SETBACK_TOP_Y), (x_from - 1, SETBACK_TOP_Y + SETBACK + 1)])
    .close().extrude(CLIP_PROUD + wall))

# -- interfaces, cut last: the wrist holder's (the servo's envelope and screws, through the clip too) --
result = holder["interfaces"](tube)
