"""Open Duck Mini v2 speaker interface, written from its STEP: interfaces exact, the body simple.

A square plate in the speaker stand's pocket, screwed through to the stand at its corners; the speaker's
opening in its middle, and six clips standing out of its outer face round the opening to hold the speaker.

Frame: the speaker stand's (x', y', z), turned S.SPEAKER_TURN about z from the vendor's; the plate lies in the
stand's tilted leg, its inner face on the pocket's floor.
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)


# -- interfaces -- fixed ----------------------------------------------------------------------------
# this part is not in the model: what it fits is declared
CENTRE = (56.273, -51.176, 135.701)        # the speaker's axis on the stand leg's outer face (x', y', z); not in the model: this part
PLATE_T = 1.5                              # in the leg's pocket, as deep as it; not in the model: this part
OPENING_D = 18.3                           # the speaker's; not in the model: the speaker
SCREW_SQUARE = 32.0                        # into the stand, on a square
SCREW_D = 2.7

# -- body: free -------------------------------------------------------------------------------------
PLATE_SIDE = 37.6                          # square
PLATE_CORNER_R = 2.0
CLIPS = [((-6.0, 15.75), 0.0), ((6.0, 15.75), 0.0), ((-6.0, -16.25), 0.0), ((6.0, -16.25), 0.0),
         ((16.25, -6.0), 90.0), ((16.25, 6.0), 90.0)]   # (u, v) from the centre on the plate, turned (deg)  # measured
CLIP_W = 3.0
CLIP_T = 1.2
CLIP_PROUD = 4.7                           # proud of the outer face

c, s = math.cos(math.radians(S.SPEAKER_TILT_DEG)), math.sin(math.radians(S.SPEAKER_TILT_DEG))
leg = cq.Plane(origin=CENTRE, xDir=(1, 0, 0), normal=(0, -c, s))       # outwards from the leg
side, t, r = PLATE_SIDE, PLATE_T, PLATE_CORNER_R
interface = cq.Workplane(leg).workplane(offset=-t).placeSketch(cq.Sketch().rect(side, side).vertices().fillet(r)).extrude(t)
w, ct, proud = CLIP_W, CLIP_T, CLIP_PROUD
for (u, v), turn in CLIPS:
    interface = interface.union(cq.Workplane(leg).center(u, v).transformed(rotate=(0, 0, turn)).rect(w, ct).extrude(proud))
interface = interface.cut(cq.Workplane(leg).workplane(offset=-t - 1).circle(OPENING_D / 2).extrude(t + 2))
sq, d = SCREW_SQUARE, SCREW_D
interface = interface.cut(cq.Workplane(leg).workplane(offset=-t - 1).pushPoints([(a * sq / 2, b * sq / 2) for a in (1, -1) for b in (1, -1)])
                          .circle(d / 2).extrude(t + 2))

result = interface.rotate((0, 0, 0), (0, 0, 1), S.SPEAKER_TURN)
