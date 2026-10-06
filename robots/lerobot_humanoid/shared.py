"""LeRobot humanoid: what its parts share. A part reads it with `shared(__file__)`.

Each value here is an interface two or more parts fit: change it here and every part that uses it
follows. A value only one part uses stays in that part.
"""

from yotown.gym.interfaces import Screw
from yotown.gym.standard.bearings import B6207, B6702
from yotown.gym.vendors.robstride import RS03

SMALL_BEARING = B6702                      # 15x21x4: the knee's axles, the u-joints' journals, the forearm, the hip yoke's axle
HIP_BEARING = B6207                        # 35x72x17: the hip yaw
M3 = Screw(hole_d=3.3, head_d=6.5)         # M3 through, counterbored
LEG_ACTUATOR = RS03                        # the hip pitch and the knee, in each leg

# -- mates: values two parts in one frame both fit -------------------------------------------------
# the femur's halves
FEMUR_BOLT_D = 4.4                         # the bolts through both halves, four about the hip and four about the knee actuator
FEMUR_BOLT_CIRCLE_D = LEG_ACTUATOR.front_screws.circle.d   # their circle about each axis: the actuators' flange (8-M4 on d98)
FEMUR_PINS = {4.0: [(22.51, 150.55), (41.3, 150.55)], 3.0: [(31.86, 166.89), (38.45, 288.39)]}   # the locating pins through both halves: {d: [(x, z), ...]}

# the hip housing (torso13) and its cap (torso23)
HIP_HOUSING_TILT = (-8.089, 0.2)           # the housing's axis: degrees about world x, then y
HIP_HOUSING_ORIGIN = (0.624415, -130.401386, -79.201183)   # the centre of the housing ring's bottom face, on its axis  # measured
HIP_HOUSING_BOLT_CIRCLE_D = 85.0           # the eight bolts holding the cap to the housing

# the hip yaw links (hipz12, hipz22)
HIPZ_X_DIR = (-0.5209141920043376, 0.7935827640893638, 0.31444363741178355)   # their frame's x  # measured
HIPZ_NORMAL = (0.1725050498000225, -0.26290076374103427, 0.9492761432891237)   # their frame's z, the hip yaw axis  # measured

# the torso's electronics
TORSO_CAN_PIN_PITCH = (96.0, 86.0)         # the can holder's pins on can_holder_2's standoffs (x, y)
TORSO_BOARD_PITCH = (58.09, 49.0)          # the board's holes (x, y)  # measured
TORSO_BOARD_AT = (10.03, 0.0)              # their centre  # measured
