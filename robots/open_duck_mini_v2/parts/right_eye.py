"""Open Duck Mini v2 eye (right), written from its STEP: interfaces exact, the body simple.

A plate on the head's face -- a square cut by a round, the corners between them rounded -- screwed on
from behind at four corners (blind holes); on it a stepped round boss holding the eye's lens in a
stepped opening; the boss's edges chamfered.

Frame: the vendor's (mm): the plate's back face is x = BACK; the eye lies in (y, z).
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
# this part is not in the model: what it fits is declared
CENTRE_Y = -40.0                           # on the head's eye hole; not in the model: this part
SCREW_D = 2.05
LENS_DEEP = 4.5                            # this deep; not in the model: the lens

# -- body: free -------------------------------------------------------------------------------------
SCREW_DEEP = 3.0
PLATE_SIDE = 40.0                          # a square cut by a round:
PLATE_ROUND_D = 45.0
PLATE_CORNER_R = 10.0
PLATE_T = 2.5
STEPS = [(38.0, 122.5, 124.5), (35.0, 124.5, 128.4)]   # the boss: d, x from-to
CHAMFER = 0.5
BACK = S.EYE_BACK_X

cy, cz = CENTRE_Y, S.FACE_CENTRE_Z
side, round_d, corner_r, thick = PLATE_SIDE, PLATE_ROUND_D, PLATE_CORNER_R, PLATE_T
on_back = cq.Workplane("YZ", origin=(BACK, 0, 0)).center(cy, cz)
eye = on_back.rect(side, side).extrude(thick).intersect(on_back.circle(round_d / 2).extrude(thick))
eye = eye.edges("|X").fillet(corner_r)
for d, x0, x1 in STEPS:
    eye = eye.union(cq.Workplane("YZ", origin=(x0, 0, 0)).center(cy, cz).circle(d / 2).extrude(x1 - x0).faces(">X").edges().chamfer(CHAMFER))

(d0, deep0), d1 = (S.EYE_LENS_D, LENS_DEEP), S.EYE_OPENING_D
front = STEPS[-1][2]
eye = eye.cut(cq.Workplane("YZ", origin=(BACK - 1, 0, 0)).center(cy, cz).circle(d0 / 2).extrude(deep0 + 1))
eye = eye.cut(cq.Workplane("YZ", origin=(BACK + deep0, 0, 0)).center(cy, cz).circle(d1 / 2).extrude(front - BACK))
s, d, deep = S.FACE_SCREW_SQUARE, SCREW_D, SCREW_DEEP
corners = [(cy + sy * s / 2, cz + sz * s / 2) for sy in (1, -1) for sz in (1, -1)]
eye = eye.cut(cq.Workplane("YZ", origin=(BACK - 1, 0, 0)).pushPoints(corners).circle(d / 2).extrude(deep + 1))

result = eye
