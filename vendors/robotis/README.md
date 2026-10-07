# ROBOTIS

DYNAMIXEL smart servos. [robotis.us](https://www.robotis.us/), [e-manual](https://emanual.robotis.com/)

| Part | Case W x H x D (mm) | Mass | Stall torque | No-load speed | Volts |
|---|---|---|---|---|---|
| XL330-M077-T | 20 x 34 x 26 | 18 g | 0.215 N·m at 5 V | 383 rpm at 5 V | 3.7 to 6 |
| XL330-M288-T | 20 x 34 x 26 | 18 g | 0.52 N·m at 5 V | 103 rpm at 5 V | 3.7 to 6 |
| XC330-T288-T | 20 x 34 x 26 | 23 g | 1.00 N·m at 12 V | 71 rpm at 12 V | 6.5 to 12 |
| XL430-W250-T | 28.5 x 46.5 x 34 | 57.2 g | 1.4 N·m at 11.1 V | 57 rpm at 11.1 V | 6.5 to 12 |
| XC430-W240-T | 28.5 x 46.5 x 34 | 65 g | 1.9 N·m at 12 V | 70 rpm at 12 V | 6.5 to 14.8 |
| XM430-W210-T | 28.5 x 46.5 x 34 | 82 g | 3.0 N·m at 12 V | 77 rpm at 12 V | 10 to 14.8 |
| XM430-W350-T | 28.5 x 46.5 x 34 | 82 g | 4.1 N·m at 12 V | 46 rpm at 12 V | 10 to 14.8 |
| 2XL430-W250-T (two axes) | 36 x 46.5 x 36 | 98.2 g | 1.4 N·m at 11.1 V | 57 rpm at 11.1 V | 6.5 to 12 |
| 2XC430-W250-T (two axes) | 36 x 46.5 x 36 | 102 g | 1.8 N·m at 12 V | 64 rpm at 12 V | 6.5 to 14.8 |

```python
from yotown.gym.vendors.robotis import XM430_W350, ALL

XM430_W350.stall_nm(12.0)   # 4.1
XM430_W350.stall            # ((3.8, 11.1, 2.1), (4.1, 12.0, 2.3), (4.8, 14.8, 2.7)): N m, V, A
```

Each class gives every voltage ROBOTIS lists. The torque is the **stall** torque, with the shaft held
still; it is not a load to hold continuously.

## Sources

Each model's [e-manual](https://emanual.robotis.com/docs/en/dxl/x/) page, its Specifications table
(read 2026-10-06).

**Not yet included:** the case's mounting holes and the horn's hole pattern. They are in the drawings
on each e-manual page (Reference, Drawings); a pull request adding them from those drawings is welcome.
