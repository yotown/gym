"""LeRobot humanoid big shin hat, written from its STEP: a disc on the y axis, a bore through, three
screws on the disc.

Frame: the STEP's (mm). The disc lies from y -8 to -5, centred on the y axis."""

import cadquery as cq

# -- interfaces -- fixed ----------------------------------------------------------------------------
BORE_D = 19.0
SCREW_D, SCREW_CIRCLE_D, FIRST_DEG = 2.8, 25.0, 90.0   # three, 120 deg apart; the first towards -z
DISC_Y = (-8.0, -5.0)

# -- body: free -------------------------------------------------------------------------------------
DISC_D = 30.0

# on the disc's -y face, extruding along +y: u is x, v is -z
disc_face = cq.Workplane(cq.Plane(origin=(0, DISC_Y[0], 0), xDir=(1, 0, 0), normal=(0, 1, 0)))
thickness = DISC_Y[1] - DISC_Y[0]

hat = disc_face.circle(DISC_D / 2).circle(BORE_D / 2).extrude(thickness)
result = hat.cut(disc_face.polarArray(SCREW_CIRCLE_D / 2, FIRST_DEG, 360, 3).circle(SCREW_D / 2).extrude(thickness))
