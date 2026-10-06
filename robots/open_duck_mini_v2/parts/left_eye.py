"""Open Duck Mini v2 eye (left), written from its STEP: interfaces exact, the body simple.

A round plate on the head's face with an ear at each of its four screws (blind, from behind),
each ear joined to the round by two R5 scallops; a round boss on it holds the eye's lens in a stepped
opening.

Frame: the vendor's (mm): the plate's back face is x = BACK, its front x = FRONT; it lies in (y, z).
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
# this part is not in the model: what it fits is declared
CENTRE_Y = 40.0                            # on the head's eye hole; not in the model: this part
SCREW_D = 2.2
LENS_DEEP = 0.5                            # this deep; not in the model: the lens

# -- body: free -------------------------------------------------------------------------------------
SCREW_DEEP = 3.0
PLATE_T = 4.3
CHAMFER = 0.5                              # the opening's front edge
ROUND_D, EAR_R = 35.0, 2.5                 # the plate: a round, an ear about each screw
SCALLOPS = (5.0, 22.5, 16.56)              # each corner's two arcs: r, their centres' distance from the middle, either side of the diagonal (deg)  # measured
BACK, FRONT = S.EYE_BACK_X, S.EYE_BACK_X + PLATE_T

cy, cz = CENTRE_Y, S.FACE_CENTRE_Z
side, d, deep = S.FACE_SCREW_SQUARE, SCREW_D, SCREW_DEEP
corners = [(cy + sy * side / 2, cz + sz * side / 2) for sy in (1, -1) for sz in (1, -1)]
r, dist, off = SCALLOPS
plane = cq.Workplane("YZ", origin=(BACK, 0, 0))
plate = plane.center(cy, cz).circle(ROUND_D / 2).extrude(FRONT - BACK)
for k in range(4):                         # each ear: its disc, and a wedge from the middle out to it, trimmed by the scallops
    a = math.radians(45 + 90 * k)
    sx, sz = cy + side / 2 * math.sqrt(2) * math.cos(a), cz + side / 2 * math.sqrt(2) * math.sin(a)
    rim = [(cy + ROUND_D / 2 * math.cos(a + s * math.radians(2 * off)), cz + ROUND_D / 2 * math.sin(a + s * math.radians(2 * off))) for s in (-1, 1)]
    plate = plate.union(plane.center(sx, sz).circle(EAR_R).extrude(FRONT - BACK))
    plate = plate.union(plane.polyline([(cy, cz), rim[0], (sx, sz), rim[1]]).close().extrude(FRONT - BACK))
scallops = [(cy + dist * math.cos(math.radians(45 + 90 * k + s * off)), cz + dist * math.sin(math.radians(45 + 90 * k + s * off)))
            for k in range(4) for s in (1, -1)]
eye = plate.cut(cq.Workplane("YZ", origin=(BACK - 1, 0, 0)).pushPoints(scallops).circle(r).extrude(FRONT - BACK + 2))

(d0, deep0), d1 = (S.EYE_LENS_D, LENS_DEEP), S.EYE_OPENING_D
eye = eye.cut(cq.Workplane("YZ", origin=(BACK - 1, 0, 0)).center(cy, cz).circle(d0 / 2).extrude(deep0 + 1))
eye = eye.cut(cq.Workplane("YZ", origin=(BACK + deep0, 0, 0)).center(cy, cz).circle(d1 / 2).extrude(FRONT - BACK))
eye = eye.faces(">X").edges(cq.selectors.NearestToPointSelector((FRONT, cy + S.EYE_OPENING_D / 2, cz))).chamfer(CHAMFER)
eye = eye.cut(cq.Workplane("YZ", origin=(BACK - 1, 0, 0)).pushPoints(corners).circle(d / 2).extrude(deep + 1))

result = eye
