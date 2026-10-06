"""LeRobot humanoid can holder, written from its STEP: a plate with a square recess underneath, two
walls along its x edges, and a peg leaning towards -y.

Frame: the STEP's (mm). The plate lies on z -101, centred on the z axis; symmetric about x = 0."""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
PIN_D = 3.0                                # four, through the plate: x, y
BOTTOM_Z = -101.0                          # the plate's underside, on can_holder_2's standoffs

# -- body: free -------------------------------------------------------------------------------------
RECESS = 84.4                              # square, from below
PLATE, PLATE_T = (110.0, 100.0), 8.0       # up from its underside
RECESS_DEPTH = 5.0
WALL_T, WALL_H = 4.8, 15.0                 # on the plate's top, along its x edges
PEG_D, PEG_LEAN = 7.0, 30.0                # leaning towards -y, deg from z
PEG_FOOT_Y = -35.0                         # where its axis meets the plate's top
PEG_FROM, PEG_TO = -2.05, 18.26            # along its axis from the foot  # measured

top_z = BOTTOM_Z + PLATE_T

plate = (cq.Workplane("XY", origin=(0, 0, BOTTOM_Z)).rect(*PLATE).extrude(PLATE_T)
         .faces("<Z").workplane().rect(RECESS, RECESS).cutBlind(-RECESS_DEPTH))
walls = (cq.Workplane("XY", origin=(0, 0, top_z)).rarray(PLATE[0] - WALL_T, 1, 2, 1)
         .rect(WALL_T, PLATE[1]).extrude(WALL_H))
plate = plate.union(walls)

lean = cq.Plane(origin=(0, PEG_FOOT_Y, top_z), xDir=(1, 0, 0), normal=(0, 0, 1)).rotated((PEG_LEAN, 0, 0))
plate = plate.union(cq.Workplane(lean).workplane(offset=PEG_FROM).circle(PEG_D / 2).extrude(PEG_TO - PEG_FROM))

result = plate.cut(cq.Workplane("XY", origin=(0, 0, BOTTOM_Z)).rarray(*S.TORSO_CAN_PIN_PITCH, 2, 2).circle(PIN_D / 2).extrude(PLATE_T))
