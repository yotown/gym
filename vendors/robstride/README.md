# RobStride

Quasi-direct-drive actuators. [robstride.com](https://www.robstride.com/)

| Part | Rated / peak torque | Reduction | Mass | Used in |
|---|---|---|---|---|
| RS00 | 5 / 14 N·m | 10 | 310 g | |
| RS02 | 6 / 17 N·m | 7.75 | 405 g | |
| RS03 | 20 / 60 N·m | 9 | 880 g | LeRobot humanoid (legs) |
| RS05 | 1.6 / 5.5 N·m | 7.75 | 191 g | |

```python
from yotown.gym.vendors.robstride import RS03, ALL

RS03.front_screws   # the housing's bolt circle on the output side
ALL                 # every actuator, for a design search over them
```

Each class has the housing's diameter and length, the rotor's diameter, and the screw and pin patterns
on the rotor and the housing's front and back faces.

## Sources

RobStride's user manuals,
[github.com/RobStride/Product_Information](https://github.com/RobStride/Product_Information):
section 1.1 for the outline and mounting dimensions (manuals 260713), section 1.3 or the electrical
characteristics for the ratings (RS00 and RS03: manual 260713; RS02 and RS05: manual 251112).

Only the hole patterns the manuals dimension are given. Where each face sits along the axis is not
included yet, and the first holes' angles are as RobStride's STEP has them, about the output axis.
