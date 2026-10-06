"""LeRobot humanoid hip yaw cap (torso23), written from its STEP: a flange bolted under the pelvis
bar's bearing housing (torso13), and a hub below it.

Frame: torso13's housing frame -- on the housing's axis, which leans 8.089 deg toward the bar's
middle and 0.2 deg sideways; its origin the centre of the housing ring's bottom face, z up the axis.
The cap hangs below it, from z 0 down."""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)
M3 = S.M3

# -- interfaces -- fixed: torso13's housing --------------------------------------------------------
BOLT_D, BOLT_FIRST_DEG = 4.3, 22.94        # eight, 45 deg apart, the housing's bolts  # measured

# -- interfaces -- fixed: what the hub carries -----------------------------------------------------
SEAT_D = 57.0                             # the bearing's seat; not in the model: the bearing
SEAT_DEPTH = 10.0                         # from the hub's bottom
CBORE_DEPTH = 17.0                        # not in the model: the M3 screws
SCREW_CIRCLE_D, SCREW_FIRST_DEG = 50.0, 0.44     # 60 deg apart  # measured
FLANGE_D = 102.0
HUB_BOTTOM = -30.0

# -- body: free -------------------------------------------------------------------------------------
BORE_D, BORE_TO = 40.0, -20.0             # the bore above the seat, inside the bearing
FLANGE_T = 6.0                            # under the housing
HUB_D = 67.0                              # the hub's outside

housing = cq.Plane(origin=S.HIP_HOUSING_ORIGIN, xDir=(1, 0, 0), normal=(0, 0, 1)).rotated((*S.HIP_HOUSING_TILT, 0))


def on_housing(z):
    return cq.Workplane(housing).workplane(offset=z)


cap = on_housing(-FLANGE_T).circle(FLANGE_D / 2).extrude(FLANGE_T)
cap = cap.union(on_housing(HUB_BOTTOM).circle(HUB_D / 2).extrude(-FLANGE_T - HUB_BOTTOM))
cap = cap.cut(on_housing(BORE_TO).circle(BORE_D / 2).extrude(-BORE_TO))
cap = cap.cut(on_housing(HUB_BOTTOM).circle(SEAT_D / 2).extrude(SEAT_DEPTH))
cap = cap.cut(on_housing(-FLANGE_T).polarArray(S.HIP_HOUSING_BOLT_CIRCLE_D / 2, BOLT_FIRST_DEG, 360, 8).circle(BOLT_D / 2).extrude(FLANGE_T))
screws = on_housing(0).polarArray(SCREW_CIRCLE_D / 2, SCREW_FIRST_DEG, 360, 6)
cap = cap.cut(screws.circle(M3.head_d / 2).extrude(-CBORE_DEPTH))
result = cap.cut(screws.circle(M3.hole_d / 2).extrude(BORE_TO))
