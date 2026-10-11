"""Flamingo nape: the plate closing the skull's back, flush in its opening, round the roll bracket's
shaft boss (the skull rolls about it); two screws forward into the skull's bosses; a notch at its foot
for the SG90's cable. Not in the model: the two M2 screws, the cable.

Frame: the Duck's vendor frame (mm), as the skull's: the roll axis along x through (ROLL_Y, ROLL_Z).
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)

# -- interfaces -- fixed ----------------------------------------------------------------------------
ROLL_Y, ROLL_Z = S.ROLL_Y, S.ROLL_Z
NAPE_X, NAPE_T = S.NAPE_X, S.NAPE_T  # its back face, flush with the skull's; its front on the bosses
SCREWS_Y = S.NAPE_SCREWS_Y              # its two screws, each side, at the roll axis's height
SCREW_D = S.CLEARANCE["M2"].hole_d

# -- body: free -------------------------------------------------------------------------------------
FIT = 0.2                                  # inside the skull's opening, this clear all round
BOSS_CLEAR = 1.0                           # round the bracket's shaft boss
CABLE_NOTCH_W = 5.0                        # the cable's notch at the foot
CABLE_NOTCH_DEEP = 3.0

r = S.skull_r(NAPE_X, S.SKULL_WALL) - FIT     # the opening's inside at the back face
plate = cq.Workplane("YZ", origin=(NAPE_X, 0, 0)).center(ROLL_Y, ROLL_Z).circle(r).circle(S.SHAFT_BOSS_D / 2 + BOSS_CLEAR).extrude(NAPE_T)
plate = plate.cut(cq.Workplane("YZ", origin=(NAPE_X - 1, 0, 0)).center(ROLL_Y, ROLL_Z - r).rect(CABLE_NOTCH_W, 2 * CABLE_NOTCH_DEEP).extrude(NAPE_T + 2))

# -- interfaces, cut last -------------------------------------------------------------------------
plate = plate.cut(cq.Workplane("YZ", origin=(NAPE_X - 1, 0, 0)).pushPoints([(ROLL_Y + s * SCREWS_Y, ROLL_Z) for s in (1, -1)])
                  .circle(SCREW_D / 2).extrude(NAPE_T + 2))
result = plate
