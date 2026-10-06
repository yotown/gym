"""LeRobot humanoid u-joint cross, written from its STEP: the journals, the pin and the hats' screws
exact, the body free.

Frame: the STEP's (mm). Two arms crossing at the origin: along x, ending in journals; along y, round
at its ends (the spacers seat on that round) and pinned through. Each journal end takes a hat
(ujoint_hat_small_12): three screws on its circle."""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)
SMALL_BEARING = S.SMALL_BEARING

# -- interfaces -- fixed ----------------------------------------------------------------------------
JOURNAL_TO_X = 23.8                        # the journals, to either end
PIN_D = 5.0                                # along y
END_ROUND_R = 10.0                         # the y arm's ends: round about x
HAT_SCREW_D, HAT_SCREW_CIRCLE_D, HAT_FIRST_DEG = 2.3, 8.0, 108.5   # as the hat's  # measured
HAT_SCREW_DEPTH = 15.0                     # not in the model: the hats' screws
X_ARM_TO = 20.0                            # the x arm's shoulders, the journals' bearings' stops

# -- body: free -------------------------------------------------------------------------------------
ARM_D = 16.0                               # the shoulders on the bearings' inner races only: keep 15 < d < 19

cross = cq.Workplane("YZ", origin=(-X_ARM_TO, 0, 0)).circle(ARM_D / 2).extrude(2 * X_ARM_TO)
cross = cross.union(cq.Workplane("YZ", origin=(-JOURNAL_TO_X, 0, 0)).circle(SMALL_BEARING.bore / 2).extrude(2 * JOURNAL_TO_X))
y_arm = cq.Workplane("XZ", origin=(0, END_ROUND_R, 0)).circle(ARM_D / 2).extrude(2 * END_ROUND_R)
round_ends = cq.Workplane("YZ", origin=(-ARM_D, 0, 0)).circle(END_ROUND_R).extrude(2 * ARM_D)
cross = cross.union(y_arm.intersect(round_ends))
cross = cross.cut(cq.Workplane("XZ", origin=(0, END_ROUND_R, 0)).circle(PIN_D / 2).extrude(2 * END_ROUND_R))
r = HAT_SCREW_CIRCLE_D / 2
screws = [(r * math.cos(math.radians(HAT_FIRST_DEG + k * 120)), r * math.sin(math.radians(HAT_FIRST_DEG + k * 120)))
          for k in range(3)]                   # (y, z), the same at both ends
for side in (1, -1):                       # the hats' screws into each journal's end
    end = cq.Workplane(cq.Plane(origin=(side * JOURNAL_TO_X, 0, 0), xDir=(0, 1, 0), normal=(-side, 0, 0)))
    cross = cross.cut(end.pushPoints([(y, -side * z) for y, z in screws]).circle(HAT_SCREW_D / 2).extrude(HAT_SCREW_DEPTH))

result = cross
