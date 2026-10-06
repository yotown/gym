"""Open Duck Mini v2 head roll mount, written from its STEP: interfaces exact, the body simple.

A cradle over the head roll servo, open below: a block with the servo's pocket under its roof, four
tabs at its corners screwed up into the head (counterbored from below), and the servo's own screws
through the two end walls, their heads in a slot across each wall. A notch for the servo's cable, a
pocket for its flange; the bottom edges chamfered.

Frame: the vendor's (mm). The servo lies along x; z up.
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)
SERVO = S.SERVO

# -- interfaces -- fixed ----------------------------------------------------------------------------
# the block's top sits in the head's top recess
BLOCK_X = (60.0, 100.0)
BLOCK_HALF_Y = 19.37
BLOCK_TOP_Z = 167.11
# the head's top screws, through tabs either side; the head's bosses on the tabs
TAB_X = (65.0, 95.0)
TAB_Y = 27.37                              # each and its mirror in y
TAB_TOP_Z = 159.01
TAB_SCREW_D = 3.6
TAB_SCREW_HEAD_D = 5.5
TAB_SCREW_HEAD_SEAT = 2.0                  # below the tab's top
# the neck roll servo, up into the block
POCKET_X = (64.0, 96.0)                    # its case
POCKET_TOP_Z = 164.17
FLANGE_POCKET_X = (96.0, 97.9)             # its flange, past the +x end  # measured
FLANGE_POCKET_HALF_Y = 9.24
FLANGE_POCKET_TOP_Z = 158.81
CABLE_NOTCH_X = (62.9, 64.0)               # its cable, through the -x wall's foot
CABLE_NOTCH_HALF_Y = 7.0
SERVO_SCREW_Z_MINUS_X = 158.06             # z in the -x wall,
SERVO_SCREW_Z_PLUS_X = 161.81              # and in the +x wall
TAB_R = 5.0                                # each tab, round about its screw, against the head's wall

# -- body: free -------------------------------------------------------------------------------------
POCKET_HALF_Y = 15.37                      # the servo's pocket: half its width
SERVO_SCREW_TAPPED = 1.0                   # the servo's screws: tapped this deep into the wall,
SERVO_SCREW_HEAD_D = 5.5                   # their heads in a slot across the wall's outside
SERVO_SCREW_HEAD_DEEP = 3.0                # this deep
BLOCK_BOTTOM_Z = 152.01
CHAMFER = 1.0                              # the block's underside edges


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY", origin=(0, 0, z0)).center((x0 + x1) / 2, (y0 + y1) / 2).rect(x1 - x0, y1 - y0).extrude(z1 - z0)


x0, x1 = BLOCK_X
z0 = BLOCK_BOTTOM_Z
mount = box(x0, x1, -BLOCK_HALF_Y, BLOCK_HALF_Y, z0, BLOCK_TOP_Z)
for tx in TAB_X:                           # each pair of tabs: a slot across the block, round about its screws
    mount = mount.union(cq.Workplane("XY", origin=(0, 0, z0)).center(tx, 0).slot2D(2 * (TAB_Y + TAB_R), 2 * TAB_R, 90).extrude(TAB_TOP_Z - z0))
mount = mount.faces("<Z").edges().chamfer(CHAMFER)

# -- interfaces, cut last -------------------------------------------------------------------------
mount = mount.cut(box(*POCKET_X, -POCKET_HALF_Y, POCKET_HALF_Y, z0 - 1, POCKET_TOP_Z))
nx0, nx1 = CABLE_NOTCH_X
mount = mount.cut(box(nx0, nx1 + 0.01, -CABLE_NOTCH_HALF_Y, CABLE_NOTCH_HALF_Y, z0 - 1, POCKET_TOP_Z))
fx0, fx1 = FLANGE_POCKET_X
mount = mount.cut(box(fx0 - 0.01, fx1, -FLANGE_POCKET_HALF_Y, FLANGE_POCKET_HALF_Y, z0 - 1, FLANGE_POCKET_TOP_Z))
pts = [(tx, s * TAB_Y) for tx in TAB_X for s in (1, -1)]
below = cq.Workplane("XY", origin=(0, 0, z0 - 1))
mount = mount.cut(below.pushPoints(pts).circle(TAB_SCREW_D / 2).extrude(TAB_TOP_Z - z0 + 2))
mount = mount.cut(below.pushPoints(pts).circle(TAB_SCREW_HEAD_D / 2).extrude(TAB_TOP_Z - TAB_SCREW_HEAD_SEAT - z0 + 1))
for s, z in ((-1, SERVO_SCREW_Z_MINUS_X), (1, SERVO_SCREW_Z_PLUS_X)):
    wall_out = x1 if s > 0 else x0
    inward = cq.Workplane("YZ", origin=(wall_out + (1 if s > 0 else -1), 0, 0))
    mount = mount.cut(inward.pushPoints([(-SERVO.tab_half_pitch, z), (SERVO.tab_half_pitch, z)]).circle(S.SERVO_SCREW_D / 2)
                      .extrude(-s * (1 + SERVO_SCREW_HEAD_DEEP + SERVO_SCREW_TAPPED)))
    mount = mount.cut(inward.center(0, z).slot2D(2 * SERVO.tab_half_pitch + SERVO_SCREW_HEAD_D, SERVO_SCREW_HEAD_D).extrude(-s * (1 + SERVO_SCREW_HEAD_DEEP)))
result = mount
