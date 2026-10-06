"""LeRobot humanoid upper-body bearing holder, written from its STEP: a ring that seats a 47 mm
bearing from below behind a lip, and six counterbored M3 screws from the top.

Frame: on the ring's top face, its axis the normal, x towards the first screw. The axis is tilted in
the STEP's frame, so the frame is measured; everything else is an offset in it. The counterbores
break out through the outer wall, as the STEP's do."""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)
M3 = S.M3

# -- frame: measured --------------------------------------------------------------------------------
TOP_CENTRE = (161.932, 25.779, 87.545)          # measured
AXIS = (0.7809, 0.1240, 0.6123)                 # bottom face to top face  # measured
FIRST_SCREW_DIR = (-0.541, 0.6243, 0.5635)      # measured

# -- interfaces -- fixed ----------------------------------------------------------------------------
SEAT_D = 47.0                                   # the bearing, seated from below; not in the model: the bearing
LIP_D, LIP_T = 43.0, 3.0                        # holds it, at the top; not in the model: the bearing
CBORE_DEPTH = 5.0                          # counterbored; not in the model: the M3 screws
BOLT_CIRCLE_D, SCREWS = 60.0, 6
OUTER_D = 65.0                                  # in the upper body's bore
THICKNESS = 12.0                                # on its seat there

# -- body: free -------------------------------------------------------------------------------------

top = cq.Workplane(cq.Plane(origin=TOP_CENTRE, xDir=FIRST_SCREW_DIR, normal=AXIS))

ring = top.circle(OUTER_D / 2).circle(LIP_D / 2).extrude(-THICKNESS)
ring = ring.cut(top.workplane(offset=-THICKNESS).circle(SEAT_D / 2).extrude(THICKNESS - LIP_T))
result = ring.copyWorkplane(top).polarArray(BOLT_CIRCLE_D / 2, 0, 360, SCREWS).cboreHole(M3.hole_d, M3.head_d, CBORE_DEPTH)
