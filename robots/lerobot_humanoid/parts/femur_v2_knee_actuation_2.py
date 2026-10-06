"""LeRobot humanoid knee actuation lever, written from its STEP: a flange on the actuator, a lever to
an eye, and a stub axle through the eye for the knee rods' bearings.

Frame: on the lever's front face (y 5), its normal -y, the origin on the actuator's axis (x 0,
z 224); the plane's x is the STEP's x, its y the STEP's z."""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)
SMALL_BEARING = S.SMALL_BEARING

# -- interfaces -- fixed ----------------------------------------------------------------------------
ACTUATOR_AT = (0.0, 5.0, 224.0)            # its axis along y, through this point on the front face
SCREW_D, CBORE_D, CBORE_DEPTH = 4.5, 7.5, 7.0   # six M4, counterbored from the front
SCREW_CIRCLE_D, SCREW_FIRST_DEG = 30.37, 32.9    # 60 deg apart  # measured
EYE_PITCH, EYE_DEG = 50.0, 206.07          # the eye from the actuator's axis  # measured
SHOULDER_HALF = 6.0                        # the shoulders' faces, the bearings' stops, either side of the lever's middle
LEVER_T = 10.0
FLANGE_T = 7.0                             # the disc behind the lever, on the actuator

# -- body: free -------------------------------------------------------------------------------------
AXLE_HALF = 11.0                           # the axle, either side of the lever's middle: at least SHOULDER_HALF + the bearings' 4 mm
SHOULDER_D = 18.0                          # on the bearings' inner races only: keep 15 < d < 19
DISC_D = 50.0
EYE_D = 18.0

front = cq.Workplane(cq.Plane(origin=ACTUATOR_AT, xDir=(1, 0, 0), normal=(0, -1, 0)))
eye = (EYE_PITCH * math.cos(math.radians(EYE_DEG)), EYE_PITCH * math.sin(math.radians(EYE_DEG)))
middle = front.workplane(offset=LEVER_T / 2)

outline = cq.Sketch().arc((0, 0), DISC_D / 2, 0, 360).arc(eye, EYE_D / 2, 0, 360).hull()
lever = front.placeSketch(outline).extrude(LEVER_T)
lever = lever.union(front.workplane(offset=LEVER_T).circle(DISC_D / 2).extrude(FLANGE_T))
lever = lever.union(middle.workplane(offset=-SHOULDER_HALF).center(*eye).circle(SHOULDER_D / 2).extrude(2 * SHOULDER_HALF))
lever = lever.union(middle.workplane(offset=-AXLE_HALF).center(*eye).circle(SMALL_BEARING.bore / 2).extrude(2 * AXLE_HALF))

screws = front.polarArray(SCREW_CIRCLE_D / 2, SCREW_FIRST_DEG, 360, 6)
lever = lever.cut(screws.circle(SCREW_D / 2).extrude(LEVER_T + FLANGE_T))
result = lever.cut(screws.circle(CBORE_D / 2).extrude(CBORE_DEPTH))
