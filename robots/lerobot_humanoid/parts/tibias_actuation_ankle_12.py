"""LeRobot humanoid ankle actuation link, written from its STEP: a boss on the actuator, an arm to
an eye, the arm's outline the hull of the boss and eye circles.

Frame: the STEP's (mm). The boss's axis runs along y through (x 0, z 154); the eye is along +x.
The boss stands proud of the arm on -y."""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)
M3 = S.M3

# -- interfaces -- fixed ----------------------------------------------------------------------------
BOSS_AXIS_Z = 154.0
M3_CIRCLE_D, M3_FIRST_DEG = 24.0, 0.0      # six, 60 deg apart: the actuator's screws
PIN_D, PIN_CIRCLE_D, PIN_FIRST_DEG = 4.0, 19.0, 30.0   # three, 120 deg apart
EYE_PITCH, EYE_BORE_D = 50.0, 5.0                      # the rod's pin, from the boss's axis
BOSS_D = 32.0
BOSS_Y = (41.0, 56.0)                      # the boss's faces; the arm's -y face (top shared)
ARM_FROM_Y = 46.0

# -- body: free -------------------------------------------------------------------------------------
EYE_D = 10.0


def across(y):
    """A plane at that y, on the boss's axis, extruding along +y: u is x, v is -z."""
    return cq.Workplane(cq.Plane(origin=(0, y, BOSS_AXIS_Z), xDir=(1, 0, 0), normal=(0, 1, 0)))


outline = cq.Sketch().arc((0, 0), BOSS_D / 2, 0, 360).arc((EYE_PITCH, 0), EYE_D / 2, 0, 360).hull()
link = across(ARM_FROM_Y).placeSketch(outline).extrude(BOSS_Y[1] - ARM_FROM_Y)
link = link.union(across(BOSS_Y[0]).circle(BOSS_D / 2).extrude(BOSS_Y[1] - BOSS_Y[0]))

depth = BOSS_Y[1] - BOSS_Y[0]
link = link.cut(across(BOSS_Y[0]).polarArray(M3_CIRCLE_D / 2, M3_FIRST_DEG, 360, 6).circle(M3.hole_d / 2).extrude(depth))
link = link.cut(across(BOSS_Y[0]).polarArray(PIN_CIRCLE_D / 2, PIN_FIRST_DEG, 360, 3).circle(PIN_D / 2).extrude(depth))
result = link.cut(across(BOSS_Y[0]).center(EYE_PITCH, 0).circle(EYE_BORE_D / 2).extrude(depth))
