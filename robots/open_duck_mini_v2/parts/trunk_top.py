"""Open Duck Mini v2 trunk top, written from its STEP: interfaces exact, the body simple.

The frame holding the two hip yaw servos: a bottom plate round both hip axes (the horns' clearance), a
back wall and two strips over each servo's bay, a box between the bays with the top plate over it; a deck
down the middle, forward onto the trunk bottom's column (two screws, a pocket for its tab, a lug either side)
and back towards the tail. Each servo sits between the bottom plate and the top plate, screwed through both.

Frame: the vendor's (mm): z up; the hip yaw axes are vertical through (0, +-S.TRUNK_HIP_Y).
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)
SERVO = S.SERVO

# -- interfaces -- fixed ----------------------------------------------------------------------------
# the hip yaw servos: the frame holds them on every side
HORN_CLEAR_D = 20.95                       # round each hip's horn, through the bottom plate
SERVO_UNDER_Z = -15.1                      # each servo stands on the bottom plate
BAY_INNER_Y = 22.63                        # its inner side, against the box between the bays (|y|)
BOX_X = (-38.0, 8.0)                       # the box: from-to
DECK_HALF_Y = 23.0                         # the deck's sides, against the servos' cases
DECK_TOP_Z = -10.0                         # the deck's top, under the servos' ears
LUGS_Y = (16.0, 22.63)                     # the lugs either side on the deck's front, against the servos: |y| from-to
SERVO_SCREW_X_TOP = (-32.75, -8.3)         # through the top plate at these x,
SERVO_SCREW_X_BOTTOM = (-29.0, -8.3)       # through the bottom plate at these x
SERVO_SCREW_HEAD_D = 4.0
SERVO_SCREW_HEAD_SEAT = 2.0                # into the bottom plate from outside
TOP_PLATE_UNDER_Z = 18.9                   # the top plate's underside, on the servos' tops
# the trunk bottom's column, under the deck
COLUMN_SEAT_Z = -20.1                      # the bottom plate's underside, on the column
TONGUE_SCREW_X = 24.28                     # down into the column's forward reach,
TONGUE_SCREW_PITCH = 14.0                  # (y)
TONGUE_SCREW_D = 3.2
TONGUE_SCREW_HEAD_D = 6.5
TONGUE_SCREW_HEAD_SEAT = 7.1               # above the column's top
TAB_BACK_X = -13.29                        # the column's tab, in a pocket under the box: its back face,
TAB_POCKET_HALF_Y = 10.0                   # the pocket's half width

# -- body: free -------------------------------------------------------------------------------------
TOP_PLATE_T = 2.0                          # the top plate over the servos: this thick
BOTTOM_X = (-40.0, -5.0)                   # the bottom plate under the bays: x from-to,
BOTTOM_HALF_Y = 50.0                       # half its width
BOTTOM_BACK_X = -44.71                     # and back past the wall in the middle, to here,
BOTTOM_BACK_HALF_Y = 25.4                  # this wide there, its corners at 45 deg
BACK_WALL_X = (-40.0, -37.0)
TOP_STRIPS_X = [(-40.0, -17.0), (-9.0, -5.0)]   # the top plate over the bays, where the servos' top screws are
TOP_OVER_BOX_X = (-40.0, -1.0)             # and solid over the box
DECK_X = (-40.0, 35.0)                     # the deck down the middle, to the front
REAR_X = (-90.0, -40.0)                    # towards the tail:
REAR_HALF_Y = 25.0
REAR_Z = (-17.1, -9.1)
REAR_CORNER_R = 5.0
BOX_CHAMFER = 6.0                          # the box's top front edge
LUGS_X = (8.0, 35.0)
LUGS_TOP_Z = 0.0
TAB_POCKET_FRONT_X = 19.4                  # the tab's pocket, forward to,  # measured
TAB_POCKET_DEEP = 5.0                      # and up into the box (clear of the tab's top)
TONGUE_PILOT_FROM_Z = -21.1                # the tongue screws run down from here (through the bottom plate)

bottom_z0, bottom_z1 = COLUMN_SEAT_Z, SERVO_UNDER_Z
top_z0, top_z1 = TOP_PLATE_UNDER_Z, TOP_PLATE_UNDER_Z + TOP_PLATE_T


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY", origin=(0, 0, z0)).center((x0 + x1) / 2, (y0 + y1) / 2).rect(x1 - x0, y1 - y0).extrude(z1 - z0)


bx0, bx1 = BOTTOM_X
trunk = box(bx0, bx1, -BOTTOM_HALF_Y, BOTTOM_HALF_Y, bottom_z0, bottom_z1)
ky0 = BOTTOM_BACK_HALF_Y + (bx0 - BOTTOM_BACK_X)
trunk = trunk.union(cq.Workplane("XY", origin=(0, 0, bottom_z0))
                    .polyline([(bx0, ky0), (BOTTOM_BACK_X, BOTTOM_BACK_HALF_Y), (BOTTOM_BACK_X, -BOTTOM_BACK_HALF_Y), (bx0, -ky0)])
                    .close().extrude(bottom_z1 - bottom_z0))
trunk = trunk.union(box(*BACK_WALL_X, -BOTTOM_HALF_Y, BOTTOM_HALF_Y, bottom_z0, top_z1))
for x0, x1 in TOP_STRIPS_X:
    trunk = trunk.union(box(x0, x1, -BOTTOM_HALF_Y, BOTTOM_HALF_Y, top_z0, top_z1))
trunk = trunk.union(box(*TOP_OVER_BOX_X, -BAY_INNER_Y, BAY_INNER_Y, top_z0, top_z1))
trunk = trunk.union(box(*DECK_X, -DECK_HALF_Y, DECK_HALF_Y, bottom_z0, DECK_TOP_Z))
rx0, rx1 = REAR_X
trunk = trunk.union(box(rx0, rx1 + 1, -REAR_HALF_Y, REAR_HALF_Y, *REAR_Z).edges("|Z").edges("<X").fillet(REAR_CORNER_R))
ox0, ox1 = BOX_X
trunk = trunk.union(box(ox0, ox1, -BAY_INNER_Y, BAY_INNER_Y, bottom_z0, top_z0).edges(
    cq.selectors.BoxSelector((ox1 - 0.1, -BAY_INNER_Y - 1, top_z0 - 0.1), (ox1 + 0.1, BAY_INNER_Y + 1, top_z0 + 0.1))).chamfer(BOX_CHAMFER))
lx0, lx1 = LUGS_X
ly0, ly1 = LUGS_Y
for s in (1, -1):
    trunk = trunk.union(box(lx0, lx1, min(s * ly0, s * ly1), max(s * ly0, s * ly1), DECK_TOP_Z - 0.01, LUGS_TOP_Z))
for hy in (S.TRUNK_HIP_Y, -S.TRUNK_HIP_Y):
    trunk = trunk.cut(cq.Workplane("XY", origin=(0, 0, bottom_z0 - 1)).center(0, hy).circle(HORN_CLEAR_D / 2).extrude(bottom_z1 - bottom_z0 + 2))

# -- interfaces, cut last -------------------------------------------------------------------------
ys = [s * (S.TRUNK_HIP_Y + d) for d in (-SERVO.tab_half_pitch, SERVO.tab_half_pitch) for s in (1, -1)]


def screws(xs, z_in, z_out, outward, seat):
    """The servos' screws through a plate, counterbored from outside down to seat (outward: +1 the top, -1 the bottom)."""
    global trunk
    pts = [(x, y) for x in xs for y in ys]
    trunk = trunk.cut(cq.Workplane("XY", origin=(0, 0, min(z_in, z_out) - 1)).pushPoints(pts).circle(S.SERVO_SCREW_D / 2).extrude(abs(z_out - z_in) + 2))
    trunk = trunk.cut(cq.Workplane("XY", origin=(0, 0, seat)).pushPoints(pts).circle(SERVO_SCREW_HEAD_D / 2).extrude(z_out - seat + outward))


screws(SERVO_SCREW_X_TOP, top_z0, top_z1, 1, top_z0)        # the heads' holes run through the top plate, to the servos
screws(SERVO_SCREW_X_BOTTOM, bottom_z1, bottom_z0, -1, bottom_z0 + SERVO_SCREW_HEAD_SEAT)
pts = [(TONGUE_SCREW_X, TONGUE_SCREW_PITCH / 2), (TONGUE_SCREW_X, -TONGUE_SCREW_PITCH / 2)]
seat = COLUMN_SEAT_Z + TONGUE_SCREW_HEAD_SEAT
trunk = trunk.cut(cq.Workplane("XY", origin=(0, 0, TONGUE_PILOT_FROM_Z)).pushPoints(pts).circle(TONGUE_SCREW_D / 2).extrude(DECK_TOP_Z - TONGUE_PILOT_FROM_Z + 1))
trunk = trunk.cut(cq.Workplane("XY", origin=(0, 0, seat)).pushPoints(pts).circle(TONGUE_SCREW_HEAD_D / 2).extrude(DECK_TOP_Z - seat + 1))
ax0, ax1 = TAB_BACK_X, TAB_POCKET_FRONT_X
trunk = trunk.cut(box(ax0, ax1, -TAB_POCKET_HALF_Y, TAB_POCKET_HALF_Y, COLUMN_SEAT_Z - 1, COLUMN_SEAT_Z + TAB_POCKET_DEEP))

result = trunk
