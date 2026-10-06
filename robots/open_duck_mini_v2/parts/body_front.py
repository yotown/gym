"""Open Duck Mini v2 body front, written from its STEP: interfaces exact, the body simple.

The front plate of the body: the body's section (S.BODY_SECTION: an octagon, its top corners cut at 45 deg and its
bottom sides drawn in), its front edges chamfered; eight screws into the body's middle, counterbored from
the front.

Frame: the vendor's (mm): x forward, the plate's back face on the body's middle at x = JOINT_X; the section
in (y, z).
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
JOINT_X = 55.0                             # the face on the body's middle
SCREW_D = 3.5
SCREW_HEAD_D = 6.5
SCREW_HEAD_SEAT = 3.0                      # in front of the joint

# -- body: free -------------------------------------------------------------------------------------
PLATE_T = 10.0
CHAMFER = 3.0                              # the front's edges

front = cq.Workplane("YZ", origin=(JOINT_X, 0, 0)).polyline(S.BODY_SECTION).close().extrude(PLATE_T).faces(">X").edges().chamfer(CHAMFER)

# -- interfaces, cut last -------------------------------------------------------------------------
pts = [(s * y, z) for y, z in S.BODY_SCREW_YZ for s in (1, -1)]
front = front.cut(cq.Workplane("YZ", origin=(JOINT_X - 1, 0, 0)).pushPoints(pts).circle(SCREW_D / 2).extrude(PLATE_T + 2))
front = front.cut(cq.Workplane("YZ", origin=(JOINT_X + SCREW_HEAD_SEAT, 0, 0)).pushPoints(pts).circle(SCREW_HEAD_D / 2).extrude(PLATE_T))

result = front
