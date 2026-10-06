"""Open Duck Mini v2 hip roll motor's bottom, written from its STEP: interfaces exact, the body simple.

A cradle under the hip roll servo: a floor on a journal (the boss below, on the hip yaw axis, turning in
the trunk's bearing), and two walls up the servo's case, their outer foot corners rounded; at one end two
tabs take the case's screws. The walls' far top corners rounded.

Frame: the vendor's (mm). The hip yaw axis is vertical (z) through YAW; the walls are at the y sides.
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)
SERVO = S.SERVO

# -- interfaces -- fixed ----------------------------------------------------------------------------
JOURNAL_D = 19.9                           # the boss below the floor, in the trunk's bearing
BEARING_SEAT_Z = -78.175                   # the floor's underside, on the bearing
SERVO_SEAT_Z = -75.175                     # the floor's top: the roll servo stands on it
CASE_SPAN = 24.94                          # the servo's case between the walls (y)
CASE_SCREW_Z = -56.765
TABS_X = -16.0                             # the tabs' inner face, against the case's ears
TAB_T = 1.5                                # each tab's thickness (x): close by the roll link
WALL = 2.9                                 # the walls, and their rounded feet, pass close over the bearing's outer ring
FOOT_R = 3.0                               # the walls' outer foot corners (about x)

# -- body: free -------------------------------------------------------------------------------------
X_TO = 14.5                                # the walls' far end
JOURNAL_LONG = 7.0                         # the journal's length
TOP_Z = -53.765                            # the walls' top
TOP_R = 3.0                                # their far top corners (about y)
TAB_H = 6.0                                # each tab: high (z),
TAB_END_R = 3.0                            # its end round

inner = CASE_SPAN / 2
outer = inner + WALL
mid_x = (TABS_X + X_TO) / 2
walls = (cq.Workplane("XY", origin=(0, 0, BEARING_SEAT_Z)).center(mid_x, S.HIP_YAW_Y).rect(X_TO - TABS_X, 2 * outer).extrude(TOP_Z - BEARING_SEAT_Z)
         .cut(cq.Workplane("XY", origin=(0, 0, SERVO_SEAT_Z)).center(mid_x, S.HIP_YAW_Y).rect(X_TO - TABS_X + 2, 2 * inner).extrude(TOP_Z - BEARING_SEAT_Z)))
cradle = walls.edges(cq.selectors.BoxSelector((TABS_X - 1, S.HIP_YAW_Y - outer - 0.1, BEARING_SEAT_Z - 0.1), (X_TO + 1, S.HIP_YAW_Y + outer + 0.1, BEARING_SEAT_Z + 0.1))) \
    .edges("|X").fillet(FOOT_R)
cradle = cradle.edges(cq.selectors.BoxSelector((X_TO - 0.1, S.HIP_YAW_Y - outer - 1, TOP_Z - 0.1), (X_TO + 0.1, S.HIP_YAW_Y + outer + 1, TOP_Z + 0.1))).fillet(TOP_R)
cradle = cradle.union(cq.Workplane("XY", origin=(0, 0, BEARING_SEAT_Z - JOURNAL_LONG)).center(S.HIP_YAW_X, S.HIP_YAW_Y).circle(JOURNAL_D / 2).extrude(JOURNAL_LONG))

# the tabs at the -x end, inside the walls, round about their screws
z = CASE_SCREW_Z
for s in (1, -1):
    hole_y = S.HIP_YAW_Y + s * SERVO.tab_half_pitch
    tab = cq.Workplane("YZ", origin=(TABS_X - TAB_T, 0, 0)).moveTo(S.HIP_YAW_Y + s * outer, z - TAB_H / 2).lineTo(hole_y, z - TAB_H / 2) \
        .threePointArc((hole_y - s * TAB_END_R, z), (hole_y, z + TAB_H / 2)).lineTo(S.HIP_YAW_Y + s * outer, z + TAB_H / 2).close().extrude(TAB_T)
    cradle = cradle.union(tab)

# -- interfaces, cut last -------------------------------------------------------------------------
pts = [(S.HIP_YAW_Y - SERVO.tab_half_pitch, z), (S.HIP_YAW_Y + SERVO.tab_half_pitch, z)]
cradle = cradle.cut(cq.Workplane("YZ", origin=(TABS_X - 2, 0, 0)).pushPoints(pts).circle(S.SERVO_SCREW_D / 2).extrude(4))

result = cradle
