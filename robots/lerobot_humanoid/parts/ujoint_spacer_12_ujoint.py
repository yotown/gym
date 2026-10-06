"""LeRobot humanoid u-joint spacer, written from its STEP: a tube along y, its end saddled to the
u-joint's round it seats on."""

import cadquery as cq

# -- interfaces -- fixed ----------------------------------------------------------------------------
SPACER_ID = 5.5                            # on its screw
FROM_Y = -15.94                            # its flat end  # measured
SEAT_R = 10.0                              # the u-joint's round (about x, through the origin) it seats on

# -- body: free -------------------------------------------------------------------------------------
SPACER_OD = 7.0

tube = cq.Workplane("XZ", origin=(0, FROM_Y, 0)).circle(SPACER_OD / 2).circle(SPACER_ID / 2).extrude(FROM_Y)

# -- interfaces, cut last -------------------------------------------------------------------------
seat = cq.Workplane("YZ", origin=(-SPACER_OD, 0, 0)).circle(SEAT_R).extrude(2 * SPACER_OD)
result = tube.cut(seat)
