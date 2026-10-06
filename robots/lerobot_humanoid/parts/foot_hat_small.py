"""LeRobot humanoid foot hat, written from its STEP: a disc and a boss on an axis along x, a bore
through, three screws on the disc."""

import cadquery as cq

# -- interfaces -- fixed ----------------------------------------------------------------------------
AXIS_YZ = (0.0, 35.0)                      # the axis, along x
DISC_X = (45.0, 49.0)                      # the disc: its faces (x)
BOSS_FROM_X = 43.0                         # the boss's end
BORE_D = 13.0                              # through
SCREW_D = 2.8                              # three, 120 deg apart, through the disc
SCREW_CIRCLE_D = 20.0
FIRST_DEG = 90.0
DISC_D = 25.0                              # in the foot's pocket
BOSS_D = 15.5                              # in the foot's bore

# -- body: free -------------------------------------------------------------------------------------


def along_x(x_from):
    return cq.Workplane("YZ", origin=(x_from, 0, 0)).center(*AXIS_YZ)


hat = along_x(DISC_X[0]).circle(DISC_D / 2).extrude(DISC_X[1] - DISC_X[0])
hat = hat.union(along_x(BOSS_FROM_X).circle(BOSS_D / 2).extrude(DISC_X[0] - BOSS_FROM_X))

# -- interfaces, cut last -------------------------------------------------------------------------
hat = hat.cut(along_x(BOSS_FROM_X).circle(BORE_D / 2).extrude(DISC_X[1] - BOSS_FROM_X))
result = hat.cut(along_x(DISC_X[0]).polarArray(SCREW_CIRCLE_D / 2, FIRST_DEG, 360, 3).circle(SCREW_D / 2)
                 .extrude(DISC_X[1] - DISC_X[0]))
