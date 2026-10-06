"""Open Duck Mini v2 head yaw-to-roll turntable, written from its STEP: interfaces exact, the body simple.

A ring on the head yaw axis carries the head roll joint across it: at the back a block with the roll's
journal (the idler end), at the front a U-bracket round the head roll servo -- screwed to it through
both plates -- whose wall carries the roll horn's mount (the horn's bore, four screws counterbored from
inside, on a raised pad). The ring's and the bracket's outer edges chamfered or rounded.

Frame: the vendor's (mm). The yaw axis is vertical (z) through YAW (x, y); the roll axis runs along x
through ROLL (y, z).
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)
SERVO, HORN, HORN_SCREW = S.SERVO, S.HORN, S.HORN_SCREW

# -- interfaces -- fixed ----------------------------------------------------------------------------
ROLL_Y, ROLL_Z = 0.0, 129.06               # the head roll axis, along x
JOURNAL_D = 19.8                           # the roll's idler journal at the back; not in the model: the idler bearing
HORN_SEAT_X = 60.95                        # the roll horn's seat: the pad on the bracket's wall
HORN_BORE_D = 7.0
HORN_SCREW_HEAD_D = 5.5                    # counterbored from inside,
HORN_SCREW_HEAD_SEAT = 1.84                # this far behind the horn's seat
SERVO_SEAT_Z = 112.96                      # the roll servo: on the bottom plate,
SERVO_TOP_Z = 145.16                       # under the top plate
FLANGE_POCKET_X = (47.22, 49.75)           # its flange in the bottom plate's top: x,  # measured
FLANGE_POCKET_DEEP = 1.7
TOP_SLOT_W = 14.0                          # a slot along x under the top plate, round its top
TOP_SLOT_DEEP = 1.0
SERVO_SCREW_X_BOTTOM = 52.75               # its screws, through the bottom plate at this x,
SERVO_SCREW_X_TOP = 49.0                   # through the top plate at this x,
SERVO_SCREW_HEAD_D = 4.0
SERVO_SCREW_HEAD_SEAT_BOTTOM = 3.0         # below the servo's seat
SERVO_SCREW_HEAD_SEAT_TOP = 2.0            # above the servo's top
WALL_INNER_X = 55.11                       # the wall's inner face: the roll servo's end against it

# -- body: free -------------------------------------------------------------------------------------
RING_UNDER_Z = 106.96                      # the turntable's underside
JOURNAL_X = (-27.0, -20.0)                 # the journal: x from-to
FLANGE_POCKET_HALF_Y = 9.24                # the flange pocket's half width
RING_OD = 80.0
RING_ID = 57.5
BLOCK_X = (-20.0, -8.75)                   # the back block: x from-to,
BLOCK_HALF_W = 14.0                        # half its width (y) = its top's round r
BLOCK_ROUND_Z = 128.06                     # the round's centre
BRACKET_X0 = 46.0                          # the front U: from x,
BRACKET_HALF_W = 12.36                     # half its width
TOP_PLATE_T = 4.0
PAD_D = 22.0                               # the horn's pad on the wall,
PAD_PROUD = 0.95                           # proud of it
CHAMFER = 1.0
CORNER_R = 3.0

z0, z1 = RING_UNDER_Z, SERVO_SEAT_Z
t0, t1 = SERVO_TOP_Z, SERVO_TOP_Z + TOP_PLATE_T
ux0, ux1 = BRACKET_X0, HORN_SEAT_X - PAD_PROUD
uh, wall = BRACKET_HALF_W, WALL_INNER_X
ry, rz = ROLL_Y, ROLL_Z


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY", origin=(0, 0, z0)).center((x0 + x1) / 2, (y0 + y1) / 2).rect(x1 - x0, y1 - y0).extrude(z1 - z0)


ring = cq.Workplane("XY", origin=(0, 0, z0)).center(S.NECK_YAW_X, S.NECK_YAW_Y).circle(RING_OD / 2).circle(RING_ID / 2).extrude(z1 - z0)
ring = ring.faces(">Z or <Z").edges(cq.selectors.RadiusNthSelector(1)).chamfer(CHAMFER)
bx0, bx1 = BLOCK_X
block = (cq.Workplane("YZ", origin=(bx0, 0, 0)).center(ry, (z0 + BLOCK_ROUND_Z) / 2).rect(2 * BLOCK_HALF_W, BLOCK_ROUND_Z - z0).extrude(bx1 - bx0)
         .union(cq.Workplane("YZ", origin=(bx0, 0, 0)).center(ry, BLOCK_ROUND_Z).circle(BLOCK_HALF_W).extrude(bx1 - bx0)))
block = block.faces("<X or >X").edges().chamfer(CHAMFER)
jx0, jx1 = JOURNAL_X
journal = cq.Workplane("YZ", origin=(jx0, 0, 0)).center(ry, rz).circle(JOURNAL_D / 2).extrude(jx1 - jx0 + 0.5).faces("<X").chamfer(CHAMFER)
bracket = box(ux0, ux1, -uh, uh, z0, t1).cut(box(ux0 - 1, wall, -uh - 1, uh + 1, z1, t0))
bracket = bracket.edges(cq.selectors.BoxSelector((ux1 - 0.1, -uh - 1, z0 - 0.1), (ux1 + 0.1, uh + 1, z0 + 0.1))).fillet(CORNER_R)
bracket = bracket.edges(cq.selectors.BoxSelector((ux1 - 0.1, -uh - 1, t1 - 0.1), (ux1 + 0.1, uh + 1, t1 + 0.1))).fillet(CORNER_R)
bracket = bracket.union(cq.Workplane("YZ", origin=(ux1, 0, 0)).center(ry, rz).circle(PAD_D / 2).extrude(PAD_PROUD))
turntable = ring.union(block).union(journal).union(bracket)

# -- interfaces, cut last -------------------------------------------------------------------------
fx0, fx1 = FLANGE_POCKET_X
fh = FLANGE_POCKET_HALF_Y
turntable = turntable.cut(box(fx0, fx1, -fh, fh, z1 - FLANGE_POCKET_DEEP, z1 + 0.01))
# the bracket's bottom plate stops at the flange pocket where it would reach into the ring's hole
hole = cq.Workplane("XY", origin=(0, 0, z0 - 1)).center(S.NECK_YAW_X, S.NECK_YAW_Y).circle(RING_ID / 2).extrude(z1 - z0 + 1.01)
turntable = turntable.cut(box(ux0 - 1, fx0, -fh, fh, z0 - 1, z1 + 0.01).intersect(hole))
turntable = turntable.cut(box(ux0 - 1, wall, -TOP_SLOT_W / 2, TOP_SLOT_W / 2, t0 - 0.01, t0 + TOP_SLOT_DEEP))
pts = HORN.points(at=(ry, rz))
through = cq.Workplane("YZ", origin=(wall - 1, 0, 0))
turntable = turntable.cut(through.center(ry, rz).circle(HORN_BORE_D / 2).extrude(HORN_SEAT_X - wall + 2))
turntable = turntable.cut(through.pushPoints(pts).circle(HORN_SCREW.hole_d / 2).extrude(HORN_SEAT_X - wall + 2))
turntable = turntable.cut(through.pushPoints(pts).circle(HORN_SCREW_HEAD_D / 2).extrude(HORN_SEAT_X - HORN_SCREW_HEAD_SEAT - wall + 1))
for x, za, zb, seat in ((SERVO_SCREW_X_BOTTOM, z0, z1, z1 - SERVO_SCREW_HEAD_SEAT_BOTTOM), (SERVO_SCREW_X_TOP, t1, t0, t0 + SERVO_SCREW_HEAD_SEAT_TOP)):
    pts = [(x, -SERVO.tab_half_pitch), (x, SERVO.tab_half_pitch)]
    turntable = turntable.cut(cq.Workplane("XY", origin=(0, 0, min(za, zb) - 1)).pushPoints(pts).circle(S.SERVO_SCREW_D / 2).extrude(abs(zb - za) + 2))
    turntable = turntable.cut(cq.Workplane("XY", origin=(0, 0, min(za, seat))).pushPoints(pts).circle(SERVO_SCREW_HEAD_D / 2).extrude(abs(seat - za)))

result = turntable
