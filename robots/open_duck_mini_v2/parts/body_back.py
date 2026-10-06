"""Open Duck Mini v2 body back, written from its STEP: interfaces exact, the body simple.

The duck's tail: a shell that runs back from the body's section (as body_front's) to a flat back face,
its top, bottom and sides sloping in; inside it the battery bay -- a box behind the lid's opening -- and on
its front edge eight bosses taking the screws from the body's middle. The battery lid lies on the bay's
front face.

Frame: the vendor's (mm): the shell runs back along -x from its joint with the middle; the section in (y, z).
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
JOINT_X = -95.0                            # the face on the body's middle
SCREW_D = 3.0
LID_SEAT_X = -100.0                        # the bay's front face: the battery lid lies on it
BAY_BACK_X = -120.625                      # the battery bay inside: its back,
BAY_HALF_W = 20.7                          # its half width (y),
BAY_Z = (-70.233, 6.167)                   # from-to
BAY_OUTSIDE_HALF_W = 25.7                  # the bay's sides outside: the USB-C charger is mounted on one

# -- body: free -------------------------------------------------------------------------------------
SECTION = [(55.0, 21.55), (33.55, 43.0), (-33.55, 43.0), (-55.0, 21.55), (-55.0, -64.25), (-46.72, -82.0),
           (46.72, -82.0), (55.0, -64.25)]   # the body's skin (as body_front's), cut where the bottom half's floor meets it (y, z)  # measured
BACK_X = -135.0                            # the tail's back face,
TAIL_HALF_W = 15.0                         # its half width,
TAIL_Z = (-70.0, -7.0)                     # z from-to
WALL = 3.0
BAY_WALL = 5.0                             # its top, bottom and back
BOSS_D = 8.0
BOSS_DEEP = 3.0                            # each boss behind the joint (the screw's pilot as deep)
TOP_Z, SIDE_Y = SECTION[1][1], SECTION[0][0]   # the skin's top and sides
BOTTOM_Z = SECTION[5][1]


def tail(inset, front=JOINT_X):
    """The tail moved in by inset: the body's section run back, between its top and bottom slopes and its
    side slopes (each from the section's edge at the joint to the back face's)."""
    bz0, bz1 = TAIL_Z
    run = JOINT_X - BACK_X
    top, bottom, side = (TOP_Z - bz1) / run, (bz0 - BOTTOM_Z) / run, (SIDE_Y - TAIL_HALF_W) / run   # how fast each comes in
    far, near = BACK_X - 1, front + 1
    body = cq.Workplane("YZ", origin=(BACK_X, 0, 0)).polyline(SECTION).close()
    body = (body.offset2D(-inset, "intersection") if inset else body).extrude(front - BACK_X)
    dt, db, ds = inset * math.hypot(1, top), inset * math.hypot(1, bottom), inset * math.hypot(1, side)
    vertical = [(x, TOP_Z - dt - top * (JOINT_X - x)) for x in (near, far)] + [(x, BOTTOM_Z + db + bottom * (JOINT_X - x)) for x in (far, near)]
    sides = [(x, SIDE_Y - ds - side * (JOINT_X - x)) for x in (near, far)] + [(x, -(SIDE_Y - ds - side * (JOINT_X - x))) for x in (far, near)]
    body = body.intersect(cq.Workplane("XZ", origin=(0, 100, 0)).polyline(vertical).close().extrude(200))
    return body.intersect(cq.Workplane("XY", origin=(0, 0, -150)).polyline(sides).close().extrude(300))


bay_out_back = BAY_BACK_X - BAY_WALL       # the tail is solid behind the bay
cavity = tail(WALL, JOINT_X + 1).intersect(cq.Workplane("YZ", origin=(bay_out_back, 0, 0)).rect(300, 300).extrude(JOINT_X + 2 - bay_out_back))
shell = tail(0).cut(cavity)
# the bay's box: its inside and its wall, from its back to the lid's seat
b0, b1 = BAY_Z
shell = shell.union(cq.Workplane("XY", origin=(0, 0, b0 - BAY_WALL)).center((bay_out_back + LID_SEAT_X) / 2, 0)
                    .rect(LID_SEAT_X - bay_out_back, 2 * BAY_OUTSIDE_HALF_W).extrude(b1 - b0 + 2 * BAY_WALL).intersect(tail(0)))

# -- interfaces, cut last -------------------------------------------------------------------------
shell = shell.cut(cq.Workplane("XY", origin=(0, 0, b0)).center((BAY_BACK_X + LID_SEAT_X + 1) / 2, 0)
                  .rect(LID_SEAT_X + 1 - BAY_BACK_X, 2 * BAY_HALF_W).extrude(b1 - b0))
pts = [(s * y, z) for y, z in S.BODY_SCREW_YZ for s in (1, -1)]
shell = shell.union(cq.Workplane("YZ", origin=(JOINT_X - BOSS_DEEP, 0, 0)).pushPoints(pts).circle(BOSS_D / 2).extrude(BOSS_DEEP))
shell = shell.cut(cq.Workplane("YZ", origin=(JOINT_X - BOSS_DEEP - 1, 0, 0)).pushPoints(pts).circle(SCREW_D / 2).extrude(BOSS_DEEP + 2))

result = shell
