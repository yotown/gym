"""Flamingo head roll bracket: the Duck's yaw-to-roll U-bracket alone -- no ring, no back journal -- on the
head yaw servo's far end, carrying the head roll's SG90 by its shaft.

The U wraps the yaw servo's far end, screwed to its tabs through both plates as the Duck's is; the case's
end lies against the wall. On the wall's front, on the roll axis, a boss takes the SG90's shaft: a bore
over the spline, the shaft's end on the boss's floor, its screw through the wall from inside (driven
before the yaw servo goes in). Not in the model: the shaft's screw.

Frame: the Duck's vendor frame (mm), as head_yaw_to_roll's: the yaw axis vertical (z) through
(NECK_YAW_X, NECK_YAW_Y), the roll axis along x through (ROLL_Y, ROLL_Z).
"""

import runpy

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)
D = runpy.run_path(S.duck("head_yaw_to_roll"))     # the Duck's yaw-to-roll: its fits to the yaw servo, and its U's body
SERVO = D["SERVO"]

# -- interfaces -- fixed: the yaw servo (the Duck's) -------------------------------------------------
SERVO_SEAT_Z, SERVO_TOP_Z = D["SERVO_SEAT_Z"], D["SERVO_TOP_Z"]   # the case: on the bottom plate, under the top plate
WALL_INNER_X = D["WALL_INNER_X"]           # the case's end against the wall
SERVO_SCREW_X_BOTTOM, SERVO_SCREW_X_TOP = D["SERVO_SCREW_X_BOTTOM"], D["SERVO_SCREW_X_TOP"]
FLANGE_POCKET_X = D["FLANGE_POCKET_X"]
FLANGE_POCKET_DEEP = D["FLANGE_POCKET_DEEP"]
TOP_SLOT_W, TOP_SLOT_DEEP = D["TOP_SLOT_W"], D["TOP_SLOT_DEEP"]
CLEAR_R = D["RING_ID"] / 2                 # the yaw horn's frame turns inside this: the bottom plate stops at it

# -- interfaces -- fixed: the roll servo (shared.py) ----------------------------------------------------
ROLL_Y, ROLL_Z = S.ROLL_Y, S.ROLL_Z
SHAFT_TIP_X = S.SHAFT_TIP_X             # the shaft's end, on the boss's floor
SHAFT_BORE_D = S.SHAFT_BORE_D
SHAFT_SCREW_D = S.SHAFT_SCREW_D
SHAFT_SCREW_HEAD_D = 4.5                   # counterbored from the wall's inside,
SHAFT_SCREW_HEAD_SEAT = 2.5                # its head this far in from the inside face

# -- body: free -------------------------------------------------------------------------------------
RING_UNDER_Z = D["RING_UNDER_Z"]           # the bottom plate's underside
BRACKET_X0 = D["BRACKET_X0"]
SIDE_WALL = 1.2                            # outside the yaw servo's screw heads (the Duck's U leaves 0.1: it prints as a slit)
TOP_PLATE_T = D["TOP_PLATE_T"]
WALL_T = 5.0                               # the wall, in front of the case's end
BOSS_D = S.SHAFT_BOSS_D                 # the shaft's boss round its bore
BOSS_GAP = 0.3                             # short of the gear tower
CORNER_R = D["CORNER_R"]
SERVO_SCREW_HEAD_D = D["SERVO_SCREW_HEAD_D"]
SERVO_SCREW_HEAD_SEAT_BOTTOM, SERVO_SCREW_HEAD_SEAT_TOP = D["SERVO_SCREW_HEAD_SEAT_BOTTOM"], D["SERVO_SCREW_HEAD_SEAT_TOP"]

z0, z1 = RING_UNDER_Z, SERVO_SEAT_Z
uh = SERVO.tab_half_pitch + SERVO_SCREW_HEAD_D / 2 + SIDE_WALL   # the U's half width
t0, t1 = SERVO_TOP_Z, SERVO_TOP_Z + TOP_PLATE_T
x0, wall, x1 = BRACKET_X0, WALL_INNER_X, WALL_INNER_X + WALL_T
boss_end = SHAFT_TIP_X + S.SG90_SHAFT_TOP - S.SG90_TOWER_TOP - BOSS_GAP


def box(xa, xb, ya, yb, za, zb):
    return cq.Workplane("XY", origin=(0, 0, za)).center((xa + xb) / 2, (ya + yb) / 2).rect(xb - xa, yb - ya).extrude(zb - za)


bracket = box(x0, x1, -uh, uh, z0, t1).cut(box(x0 - 1, wall, -uh - 1, uh + 1, z1, t0))
for z in (z0, t1):                         # the wall's outer corners rounded
    bracket = bracket.edges(cq.selectors.BoxSelector((x1 - 0.1, -uh - 1, z - 0.1), (x1 + 0.1, uh + 1, z + 0.1))).fillet(CORNER_R)
bracket = bracket.union(cq.Workplane("YZ", origin=(x1, 0, 0)).center(ROLL_Y, ROLL_Z).circle(BOSS_D / 2).extrude(boss_end - x1))

# -- interfaces, cut last -------------------------------------------------------------------------
fx0, fx1 = FLANGE_POCKET_X
fh = D["FLANGE_POCKET_HALF_Y"]
bracket = bracket.cut(box(fx0, fx1, -fh, fh, z1 - FLANGE_POCKET_DEEP, z1 + 0.01))
turn = cq.Workplane("XY", origin=(0, 0, z0 - 1)).center(D["S"].NECK_YAW_X, D["S"].NECK_YAW_Y).circle(CLEAR_R).extrude(z1 - z0 + 1.01)
bracket = bracket.cut(box(x0 - 1, fx0, -fh, fh, z0 - 1, z1 + 0.01).intersect(turn))
bracket = bracket.cut(box(x0 - 1, wall, -TOP_SLOT_W / 2, TOP_SLOT_W / 2, t0 - 0.01, t0 + TOP_SLOT_DEEP))
for x, za, zb, seat in ((SERVO_SCREW_X_BOTTOM, z0, z1, z1 - SERVO_SCREW_HEAD_SEAT_BOTTOM), (SERVO_SCREW_X_TOP, t1, t0, t0 + SERVO_SCREW_HEAD_SEAT_TOP)):
    pts = [(x, -SERVO.tab_half_pitch), (x, SERVO.tab_half_pitch)]
    bracket = bracket.cut(cq.Workplane("XY", origin=(0, 0, min(za, zb) - 1)).pushPoints(pts).circle(D["S"].SERVO_SCREW_D / 2).extrude(abs(zb - za) + 2))
    bracket = bracket.cut(cq.Workplane("XY", origin=(0, 0, min(za, seat))).pushPoints(pts).circle(SERVO_SCREW_HEAD_D / 2).extrude(abs(seat - za)))
roll = cq.Workplane("YZ", origin=(wall - 1, 0, 0)).center(ROLL_Y, ROLL_Z)
bracket = bracket.cut(cq.Workplane("YZ", origin=(SHAFT_TIP_X, 0, 0)).center(ROLL_Y, ROLL_Z).circle(SHAFT_BORE_D / 2).extrude(boss_end - SHAFT_TIP_X + 1))
bracket = bracket.cut(roll.circle(SHAFT_SCREW_D / 2).extrude(SHAFT_TIP_X - wall + 2))
bracket = bracket.cut(roll.circle(SHAFT_SCREW_HEAD_D / 2).extrude(1 + SHAFT_SCREW_HEAD_SEAT))
result = bracket
