"""LeRobot humanoid hip x-y yoke, written from its STEP: interfaces exact, the body simple.

Frame: the vendor's (mm). Two working frames:
  top    on the hip-yaw axis (z, up), turned YAW_TURN about it: u along the hip-pitch axis's direction,
         v across. A column with the yaw bearing's screws stands on a square plate.
  pitch  on the hip-pitch axis: origin at PITCH_AT, u along PITCH_AXIS (it leans PITCH_TILT up from
         the horizontal), w up. Two legs hang from the plate to it: one holds the pitch actuator by a
         ring of M4 screws, the other the axle's bearing.
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)
SMALL_BEARING, HIP_BEARING = S.SMALL_BEARING, S.HIP_BEARING

# -- interfaces -- fixed ----------------------------------------------------------------------------
YAW_TURN = 114.254                         # the pitch axis's heading about z, deg  # measured
COLUMN_TOP = 0.0
YAW_SCREWS = (24.0, 6, 26.1, 4.2, 7.5, 5.0)    # six screws down the column: circle, count, first angle, d, head d, its seat below the top
YAW_PINS = (24.0, 3, 56.1, 4.0, 10.0)      # three holes in its top: circle, count, first angle, d, depth
PITCH_AT = (-0.3, 0.69, -109.95)           # a point on the hip-pitch axis
PITCH_AXIS = (-0.41, 0.91, 0.07)
ACTUATOR_SCREWS = (30.2, 30.0, -1.0, (0, 4, 8), 4.5)   # M4s through the actuator's leg: circle, pitch (deg), first angle, positions left out, d
LEGS = ((-46.0, -34.0), (30.5, 44.5))      # along the pitch axis: the actuator's leg, the bearing's  # measured

# -- body: free -------------------------------------------------------------------------------------
BEARING_SEAT_FLOOR = 39.6                  # the axle bearing's seat (15 x 21 x 4, its diameter the interface): its floor, along the pitch axis, clear of the bearing (the thigh's axle locates it): keep > 36.3
PLATE = ((-50.0, 42.0), (-65.0, 57.0), (-50.0, -35.0))   # in the top frame: u, v, z  # measured
PLATE_TOP_R = 5.0                          # the plate's top edges, all round  # measured
GROOVE = (79.5, 92.5, 4.0)                 # the ring groove hip_z 22 turns in: inside, outside (each 1 mm wider than the vendor's 80.5 / 91.5, for clearance), deep
LEG_TOP_W = 68.0                           # the legs' tops, up the pitch frame (into the plate)
LEG_SPAN = (-63.0, 57.0)                   # how wide they are there (v)  # measured
LEG_ROUND = 26.0                           # round the pitch axis at their foot  # measured

top = cq.Plane(origin=(0, 0, 0), xDir=(math.cos(math.radians(YAW_TURN)), math.sin(math.radians(YAW_TURN)), 0), normal=(0, 0, 1))
(u0, u1), (v0, v1), (z0, z1) = PLATE
hip = cq.Workplane(top).workplane(offset=z0).center((u0 + u1) / 2, (v0 + v1) / 2).rect(u1 - u0, v1 - v0).extrude(z1 - z0)
hip = hip.faces(">Z").edges("not(|Z)").fillet(PLATE_TOP_R)
hip = hip.cut(cq.Workplane(top).workplane(offset=z1 - GROOVE[2]).circle(GROOVE[1] / 2).circle(GROOVE[0] / 2).extrude(GROOVE[2]))
hip = hip.union(cq.Workplane(top).workplane(offset=z1).circle(HIP_BEARING.bore / 2).extrude(COLUMN_TOP - z1))

# the legs, in the pitch frame: each a slab, as wide as the plate at its top, round about the axis at its foot
a = cq.Vector(*PITCH_AXIS).normalized()
v_dir = cq.Vector(0, 0, 1).cross(a).normalized()
w_dir = a.cross(v_dir)
for lo, hi in LEGS:
    side = cq.Plane(origin=cq.Vector(*PITCH_AT) + a * lo, xDir=v_dir, normal=a)
    sk = cq.Sketch().arc((0, 0), LEG_ROUND, 0, 360).segment((LEG_SPAN[0], LEG_TOP_W), (LEG_SPAN[1], LEG_TOP_W)).hull()
    hip = hip.union(cq.Workplane(side).placeSketch(sk).extrude(hi - lo))

# -- interfaces, cut last -------------------------------------------------------------------------
c, n, first, d, head, seat = YAW_SCREWS
hip = hip.cut(cq.Workplane(top).workplane(offset=COLUMN_TOP - seat).polarArray(c / 2, first, 360, n).circle(d / 2).extrude(seat))
hip = hip.cut(cq.Workplane(top).workplane(offset=z0 - 1).polarArray(c / 2, first, 360, n).circle(head / 2).extrude(COLUMN_TOP - seat - z0 + 1))
c, n, first, d, depth = YAW_PINS
hip = hip.cut(cq.Workplane(top).workplane(offset=COLUMN_TOP - depth).polarArray(c / 2, first, 360, n).circle(d / 2).extrude(depth))
c, pitch, first, skip, d = ACTUATOR_SCREWS
lo, hi = LEGS[0]
leg = cq.Workplane(cq.Plane(origin=cq.Vector(*PITCH_AT) + a * (lo - 1), xDir=v_dir, normal=a))
pts = [(c / 2 * math.cos(math.radians(first + k * pitch)), c / 2 * math.sin(math.radians(first + k * pitch))) for k in range(12) if k not in skip]
hip = hip.cut(leg.pushPoints(pts).circle(d / 2).extrude(hi - lo + 2))
seat_from = LEGS[1][0] - 1                 # the seat: from past the leg's inner face to its floor
hip = hip.cut(cq.Workplane(cq.Plane(origin=cq.Vector(*PITCH_AT) + a * seat_from, xDir=v_dir, normal=a))
              .circle(SMALL_BEARING.od / 2).extrude(BEARING_SEAT_FLOOR - seat_from))

result = hip
