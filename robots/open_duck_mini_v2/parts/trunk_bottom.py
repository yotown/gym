"""Open Duck Mini v2 trunk bottom, written from its STEP: interfaces exact, the body simple.

The base the legs hang from: a plate round both hip yaw axes, standing on the body's floor, a bearing seat
on each axis (the bearing from above, a lip under it), its long sides drafted; four screws up into it from
below; on it a column carrying the trunk's top, reaching forward at its top on a 45 deg underside, with
two screws there and a tab on top.

Frame: the vendor's (mm): z up; the hip yaw axes are vertical through (HIP_X, +-S.TRUNK_HIP_Y).
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)
INSERT = S.INSERT

# -- interfaces -- fixed ----------------------------------------------------------------------------
HIP_X = 0.0                                # the hip yaw axes, each side
FLOOR_SEAT_Z = -88.775                     # the plate's underside, on the body's floor
BEARING_SEAT_D = 32.2                      # each hip's bearing, from the top ...
BEARING_SEAT_Z = -85.275                   # ... down to here
BEARING_LIP_D = 26.2                       # under it, through
SCREW_D = 3.2                              # ... and on into its pilot
COLUMN_TOP_Z = -20.1                       # the trunk's top stands on the column
TOP_SCREW_X = 24.28                        # down from the trunk's top into the column's forward reach
TOP_SCREW_PITCH = 14.0                     # (y)
TAB_HALF_Y = 10.0                          # the tab on the column's top, into the trunk top's pocket
TAB_H = 5.0

# -- body: free -------------------------------------------------------------------------------------
PLATE_TOP_Z = -78.775
COLUMN_X = (-19.0, 19.0)                   # the column, between the trunk top's bays
COLUMN_HALF_Y = 12.63
TAB_X = (-13.29, 2.64)                     # the tab on the column's top: from-to
PLATE_W = 38.0                             # round both hips (x),
PLATE_L = 108.0                            # end to end (y)
DRAFT_DEG = 12.0                           # its sides, all round  # measured
REACH_X = 35.36                            # the column's top reaches forward to here,
REACH_DEG = 45.0                           # its underside at this angle
FLOOR_PILOT_TOP_Z = -67.775                # the floor screws' pilots, up to here
TOP_PILOT_DEEP = 7.0                       # the top screws' pilots, below the column's top

plate = cq.Workplane("XY", origin=(0, 0, FLOOR_SEAT_Z)).slot2D(PLATE_L, PLATE_W, 90).extrude(PLATE_TOP_Z - FLOOR_SEAT_Z, taper=DRAFT_DEG)
cx0, cx1 = COLUMN_X
under = COLUMN_TOP_Z - (REACH_X - cx1) * math.tan(math.radians(REACH_DEG))
column = (cq.Workplane("XZ", origin=(0, COLUMN_HALF_Y, 0))
          .polyline([(cx0, PLATE_TOP_Z), (cx1, PLATE_TOP_Z), (cx1, under), (REACH_X, COLUMN_TOP_Z), (cx0, COLUMN_TOP_Z)]).close()
          .extrude(2 * COLUMN_HALF_Y))
tx0, tx1 = TAB_X
trunk = plate.union(column).union(cq.Workplane("XY", origin=(0, 0, COLUMN_TOP_Z)).center((tx0 + tx1) / 2, 0).rect(tx1 - tx0, 2 * TAB_HALF_Y).extrude(TAB_H))

# -- interfaces, cut last -------------------------------------------------------------------------
for hy in (S.TRUNK_HIP_Y, -S.TRUNK_HIP_Y):
    trunk = trunk.cut(cq.Workplane("XY", origin=(0, 0, BEARING_SEAT_Z)).center(HIP_X, hy).circle(BEARING_SEAT_D / 2).extrude(PLATE_TOP_Z - BEARING_SEAT_Z + 1))
    trunk = trunk.cut(cq.Workplane("XY", origin=(0, 0, FLOOR_SEAT_Z - 1)).center(HIP_X, hy).circle(BEARING_LIP_D / 2).extrude(BEARING_SEAT_Z - FLOOR_SEAT_Z + 1))
pts = [(a * S.TRUNK_FLOOR_SCREW_X / 2, b * S.TRUNK_FLOOR_SCREW_Y / 2) for a in (1, -1) for b in (1, -1)]
trunk = trunk.cut(cq.Workplane("XY", origin=(0, 0, FLOOR_SEAT_Z - 1)).pushPoints(pts).circle(SCREW_D / 2).extrude(FLOOR_PILOT_TOP_Z - FLOOR_SEAT_Z + 1))
trunk = trunk.cut(cq.Workplane("XY", origin=(0, 0, FLOOR_SEAT_Z - 1)).pushPoints(pts).circle(INSERT.hole_d / 2).extrude(INSERT.depth + 1))
pts = [(TOP_SCREW_X, TOP_SCREW_PITCH / 2), (TOP_SCREW_X, -TOP_SCREW_PITCH / 2)]
trunk = trunk.cut(cq.Workplane("XY", origin=(0, 0, COLUMN_TOP_Z + 1)).pushPoints(pts).circle(INSERT.hole_d / 2).extrude(-(INSERT.depth + 1)))
trunk = trunk.cut(cq.Workplane("XY", origin=(0, 0, COLUMN_TOP_Z + 1)).pushPoints(pts).circle(SCREW_D / 2).extrude(-(TOP_PILOT_DEEP + 1)))

result = trunk
