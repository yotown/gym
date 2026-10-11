"""Flamingo eye: a dome on a peg, pressed into a socket on the skull's side (one program, both eyes).

Frame: the eye's own (mm): z out along its axis, the origin where the peg enters the skull (shared.py's
eye_seat places it).
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)

# -- interfaces -- fixed ----------------------------------------------------------------------------
PEG_D = S.EYE_PEG_D                     # into the skull's socket

# -- body: free -------------------------------------------------------------------------------------
PEG_LONG = S.SKULL_WALL + 1.5           # through the wall and past it
EYE_D = 11.0                               # the dome: across its base,
EYE_PROUD = 3.5                            # its height out of the skull
EYE_RIM = 1.2                              # the dome stands on a band this tall (a printable edge)

cap = EYE_PROUD - EYE_RIM
ball_r = ((EYE_D / 2) ** 2 + cap ** 2) / (2 * cap)   # the cap's sphere
ball = cq.Workplane("XY").add(cq.Solid.makeSphere(ball_r, cq.Vector(0, 0, EYE_PROUD - ball_r), angleDegrees1=-90, angleDegrees2=90))
eye = ball.intersect(cq.Workplane("XY").circle(EYE_D / 2).extrude(EYE_PROUD)).union(cq.Workplane("XY").circle(EYE_D / 2).extrude(EYE_RIM + 0.01))
eye = eye.union(cq.Workplane("XY", origin=(0, 0, -PEG_LONG)).circle(PEG_D / 2).extrude(PEG_LONG + 0.01))
result = eye
