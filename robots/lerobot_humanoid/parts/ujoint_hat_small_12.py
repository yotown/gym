"""LeRobot humanoid u-joint hat, written from its STEP: a disc on the x axis, three screws on a circle."""

import cadquery as cq

# -- interfaces -- fixed ----------------------------------------------------------------------------
HAT_AT_X = -26.3                           # its face on the u-joint
SCREW_D = 2.6                              # three, 120 deg apart
SCREW_CIRCLE_D = 8.0
FIRST_DEG = 108.5                          # measured
HAT_T = 2.0                                # its back face on the u-joint too

# -- body: free -------------------------------------------------------------------------------------
HAT_D = 17.0

hat = cq.Workplane("YZ", origin=(HAT_AT_X, 0, 0)).circle(HAT_D / 2).extrude(HAT_T)

# -- interfaces, cut last -------------------------------------------------------------------------
result = hat.cut(cq.Workplane("YZ", origin=(HAT_AT_X, 0, 0)).polarArray(SCREW_CIRCLE_D / 2, FIRST_DEG, 360, 3)
                 .circle(SCREW_D / 2).extrude(HAT_T))
