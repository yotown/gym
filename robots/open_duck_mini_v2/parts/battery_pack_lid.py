"""Open Duck Mini v2 battery pack lid, written from its STEP: interfaces exact, the body simple.

A plate on the battery bay's front face in the tail: four screws at its corners (counterbored from the
body's side), a notch in each end (for the cables), and a grip standing proud into the bay against the
cells.

Frame: the vendor's (mm): the lid's face on the bay is x = SEAT_X, its other face LID_T forward; it lies
in (y, z).
"""

import cadquery as cq

# -- interfaces -- fixed ----------------------------------------------------------------------------
SEAT_X = -100.0                            # the face on the bay's front
HALF_W = 25.7                              # as the bay's outside (y)
LID_Z = (-75.233, 11.167)                  # as the bay's outside: from-to
SCREW_Y = 23.2                             # each and its mirror in y,
SCREW_Z = (-72.733, 8.667)                 # at each end
SCREW_D = 2.5
SCREW_HEAD_D = 4.0
SCREW_HEAD_SEAT = 2.0                      # off the bay's face
GRIP_PROUD = 2.5                           # the grip, proud of the seat into the bay: its face against the cells

# -- body: free -------------------------------------------------------------------------------------
LID_T = 5.0
NOTCH_HALF_W = 15.0                        # in each end, for the cables
NOTCH_DEEP = 5.0
GRIP_HALF_W = 12.5                         # the grip's size on the lid
GRIP_Z = (-57.033, -7.033)

z0, z1 = LID_Z
lid = cq.Workplane("YZ", origin=(SEAT_X, 0, 0)).center(0, (z0 + z1) / 2).rect(2 * HALF_W, z1 - z0).extrude(LID_T)
for z in (z0, z1):
    lid = lid.cut(cq.Workplane("YZ", origin=(SEAT_X - 1, 0, 0)).center(0, z).rect(2 * NOTCH_HALF_W, 2 * NOTCH_DEEP).extrude(LID_T + 2))
g0, g1 = GRIP_Z
lid = lid.union(cq.Workplane("YZ", origin=(SEAT_X - GRIP_PROUD, 0, 0)).center(0, (g0 + g1) / 2).rect(2 * GRIP_HALF_W, g1 - g0).extrude(GRIP_PROUD))

# -- interfaces, cut last -------------------------------------------------------------------------
pts = [(s * SCREW_Y, z) for s in (1, -1) for z in SCREW_Z]
lid = lid.cut(cq.Workplane("YZ", origin=(SEAT_X - 1, 0, 0)).pushPoints(pts).circle(SCREW_D / 2).extrude(LID_T + 2))
lid = lid.cut(cq.Workplane("YZ", origin=(SEAT_X + SCREW_HEAD_SEAT, 0, 0)).pushPoints(pts).circle(SCREW_HEAD_D / 2).extrude(LID_T))

result = lid
