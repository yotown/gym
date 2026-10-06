"""LeRobot humanoid can holder base, written from its STEP: a plate with a square recess on top, four
standoffs that carry the can holder, and a board's screw holes through the recess's floor.

Frame: the STEP's (mm). The plate lies on z -127.55, centred on the z axis; the standoffs end on
z -101, where the can holder's plate sits."""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
STANDOFF_TOP_Z = -101.0                    # the can holder sits on them; not in the model: torso_can_holder
PIN_D, SCREW_D = 3.0, 4.0                  # the bores, alternating: d3 on the (+x, -y) diagonal
BOARD_HOLE_D = 2.5
BOTTOM_Z = -127.55                         # the plate's underside, over the board; not in the model: the board

# -- body: free -------------------------------------------------------------------------------------
PLATE, PLATE_T = (110.0, 100.0), 8.0       # up from its underside
RECESS, RECESS_DEPTH = 84.4, 5.0           # square, from the top
STANDOFF_D = 7.0

top_z = BOTTOM_Z + PLATE_T
px, py = S.TORSO_CAN_PIN_PITCH[0] / 2, S.TORSO_CAN_PIN_PITCH[1] / 2

base = (cq.Workplane("XY", origin=(0, 0, BOTTOM_Z)).rect(*PLATE).extrude(PLATE_T)
        .faces(">Z").workplane().rect(RECESS, RECESS).cutBlind(-RECESS_DEPTH))
base = base.union(cq.Workplane("XY", origin=(0, 0, top_z)).rarray(*S.TORSO_CAN_PIN_PITCH, 2, 2)
                  .circle(STANDOFF_D / 2).extrude(STANDOFF_TOP_Z - top_z))

through = cq.Workplane("XY", origin=(0, 0, BOTTOM_Z))
height = STANDOFF_TOP_Z - BOTTOM_Z
base = base.cut(through.pushPoints([(px, -py), (-px, py)]).circle(PIN_D / 2).extrude(height))
base = base.cut(through.pushPoints([(-px, -py), (px, py)]).circle(SCREW_D / 2).extrude(height))
result = base.cut(through.center(*S.TORSO_BOARD_AT).rarray(*S.TORSO_BOARD_PITCH, 2, 2).circle(BOARD_HOLE_D / 2).extrude(PLATE_T))
