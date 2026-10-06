"""Open Duck Mini v2 hip roll motor's top, written from its STEP: interfaces exact, the body simple.

A cap over the hip roll servo, open below: a top plate on the hip yaw servo's horn (the horn's bore and
four screws on a pad on top, the screws' heads counterbored from inside), and two side walls down the roll
servo's case, screwed to it -- the two sides at different heights -- with shallow pockets for its ribs.
The walls' lower corners rounded; the outer edges chamfered.

Frame: the vendor's (mm). The hip yaw axis is vertical (z) through YAW; the walls are at x = +-INNER_HALF.
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)
SERVO, HORN, HORN_SCREW = S.SERVO, S.HORN, S.HORN_SCREW

# -- interfaces -- fixed ----------------------------------------------------------------------------
HORN_SEAT_Z = -29.79                       # the plate's underside: the yaw servo's horn on it
HORN_BORE_D = 7.0
HORN_SCREW_HEAD_SEAT = 8.0                 # above the horn's seat
CASE_HALF_X = 16.0                         # the roll servo's case between the walls: half its width (x)
CASE_SCREW_Z_PLUS_X = -36.065              # their z, in the +x wall
CASE_SCREW_Z_MINUS_X = -32.315             # and in the -x wall
PAD_TOP_Z = -19.05                         # the horn's pad on top: the trunk's horn plate on it
RIB_POCKETS = {1: (14.0, 1.1, -29.955), -1: (18.48, 1.9, -35.25)}   # the case's ribs, in each wall's inner face: long (y), deep (x), up to z  # measured

# -- body: free -------------------------------------------------------------------------------------
OUTER_X, OUTER_Y = 38.0, 28.72
TOP_Z = -22.05                             # the plate's top
FOOT_Z = -39.065                           # the walls' foot
PAD_FOOT_D = 24.0                          # the horn's pad on top, a frustum: d at its foot,
PAD_TOP_D = 20.0                           # at its top
FOOT_R = 3.0                               # the walls' lower corners (about x)
CHAMFER = 1.0

cap = cq.Workplane("XY", origin=(0, 0, FOOT_Z)).center(S.HIP_YAW_X, S.HIP_YAW_Y).rect(OUTER_X, OUTER_Y).extrude(TOP_Z - FOOT_Z)
cap = cap.edges("|Z").chamfer(CHAMFER).faces(">Z").edges().chamfer(CHAMFER)
cap = cap.cut(cq.Workplane("XY", origin=(0, 0, FOOT_Z - 1)).center(S.HIP_YAW_X, S.HIP_YAW_Y).rect(2 * CASE_HALF_X, OUTER_Y + 2).extrude(HORN_SEAT_Z - FOOT_Z + 1))
# the walls' lower corners: rounded about x
cap = cap.edges(cq.selectors.BoxSelector((S.HIP_YAW_X - OUTER_X, S.HIP_YAW_Y - OUTER_Y, FOOT_Z - 0.1), (S.HIP_YAW_X + OUTER_X, S.HIP_YAW_Y + OUTER_Y, FOOT_Z + 0.1))).edges("|X").fillet(FOOT_R)
cap = cap.union(cq.Workplane().add(cq.Solid.makeCone(PAD_FOOT_D / 2, PAD_TOP_D / 2, PAD_TOP_Z - TOP_Z, cq.Vector(S.HIP_YAW_X, S.HIP_YAW_Y, TOP_Z))))
for s, (long_, deep, up_to) in RIB_POCKETS.items():
    x0 = S.HIP_YAW_X + s * CASE_HALF_X
    cap = cap.cut(cq.Workplane("XY", origin=(0, 0, FOOT_Z - 1)).center(x0 + s * deep / 2, S.HIP_YAW_Y).rect(deep, long_).extrude(up_to - FOOT_Z + 1))

# -- interfaces, cut last -------------------------------------------------------------------------
top = PAD_TOP_Z
inside = cq.Workplane("XY", origin=(0, 0, HORN_SEAT_Z - 1))
cap = cap.cut(inside.center(S.HIP_YAW_X, S.HIP_YAW_Y).circle(HORN_BORE_D / 2).extrude(top - HORN_SEAT_Z + 2))
pts = HORN.points(at=(S.HIP_YAW_X, S.HIP_YAW_Y))
cap = cap.cut(inside.pushPoints(pts).circle(HORN_SCREW.hole_d / 2).extrude(top - HORN_SEAT_Z + 2))
cap = cap.cut(inside.pushPoints(pts).circle(HORN_SCREW.head_d / 2).extrude(HORN_SCREW_HEAD_SEAT + 1))
for s, z in ((1, CASE_SCREW_Z_PLUS_X), (-1, CASE_SCREW_Z_MINUS_X)):
    wall = cq.Workplane("YZ", origin=(S.HIP_YAW_X + s * CASE_HALF_X - (1 if s > 0 else 4), 0, 0))
    cap = cap.cut(wall.pushPoints([(S.HIP_YAW_Y - SERVO.tab_half_pitch, z), (S.HIP_YAW_Y + SERVO.tab_half_pitch, z)]).circle(S.SERVO_SCREW_D / 2).extrude(5))

result = cap
