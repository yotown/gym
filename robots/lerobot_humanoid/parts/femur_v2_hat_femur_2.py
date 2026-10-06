"""LeRobot humanoid femur hat, written from its STEP: a flange and a boss on the y axis, a bore
through, three screws on the flange."""

import cadquery as cq

# -- interfaces -- fixed ----------------------------------------------------------------------------
FLANGE_Y = (-30.0, -27.0)                  # the flange: its faces (y)
BORE_D = 12.0                              # through
SCREW_D = 2.5                              # three, 120 deg apart, through the flange
SCREW_CIRCLE_D = 19.0
FIRST_DEG = 60.0
FLANGE_D = 23.0                            # in the femur's pocket
BOSS_D = 15.2                              # in the femur's bore

# -- body: free -------------------------------------------------------------------------------------
BOSS_TO_Y = -18.5                          # the boss's end


def along_y(y_from, y_to):
    return cq.Workplane("XZ", origin=(0, y_to, 0))


hat = along_y(*FLANGE_Y).circle(FLANGE_D / 2).extrude(FLANGE_Y[1] - FLANGE_Y[0])
hat = hat.union(along_y(FLANGE_Y[1], BOSS_TO_Y).circle(BOSS_D / 2).extrude(BOSS_TO_Y - FLANGE_Y[1]))

# -- interfaces, cut last -------------------------------------------------------------------------
hat = hat.cut(along_y(FLANGE_Y[0], BOSS_TO_Y).circle(BORE_D / 2).extrude(BOSS_TO_Y - FLANGE_Y[0]))
result = hat.cut(along_y(*FLANGE_Y).polarArray(SCREW_CIRCLE_D / 2, FIRST_DEG, 360, 3).circle(SCREW_D / 2)
                 .extrude(FLANGE_Y[1] - FLANGE_Y[0]))
