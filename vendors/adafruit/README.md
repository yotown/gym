# Adafruit

Sensor and driver breakout boards. [adafruit.com](https://www.adafruit.com/)

| Part | Instance | Outline (mm) | Holes | Used in |
|---|---|---|---|---|
| [BNO085 9-DOF IMU (4754)](https://www.adafruit.com/product/4754) | `BNO085` | 25.4 x 22.86 | 20.32 x 17.78 apart, d2.5 | |
| [BNO055 9-DOF IMU, STEMMA QT (4646)](https://www.adafruit.com/product/4646) | `BNO055` | 25.4 x 20.32 | 20.32 x 15.24 apart, d2.5 | LeRobot humanoid (`torso_imu_holder`) |

```python
from yotown.gym.vendors.adafruit import BNO085

BNO085.hole_points()        # the four holes about the board's centre
```

The LeRobot humanoid's bill of materials names "BNO055 or BNO085" without a maker. Its `torso_imu_holder`
has the BNO055 STEMMA QT breakout's hole pattern, and takes it from `BNO055.holes.pitch`.

## Sources

Adafruit's open board layouts (EAGLE), from which the outline and the mounting holes are read:
[Adafruit-BNO08x-PCB](https://github.com/adafruit/Adafruit-BNO08x-PCB) and
[Adafruit-BNO055-Breakout-PCB](https://github.com/adafruit/Adafruit-BNO055-Breakout-PCB).
