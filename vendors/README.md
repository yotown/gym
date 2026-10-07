# Vendors

The parts a robot buys rather than prints: servos and actuators, boards, sensors, cameras, batteries.
Each maker has a folder here, and each part is a Python class with its dimensions, its mounting
features and its ratings.

A robot's programs use these classes, so a printed part fits the bought part it holds. Swap the servo
in a robot's `shared.py` and every part that holds it changes with it:

```python
from yotown.gym.vendors.robstride import RS02, RS03

LEG_ACTUATOR = RS03          # one line: the bolt circles, bores and clearances follow
```

That also makes each part a choice a design search can make: a robot can be built and simulated with
each actuator in a list, and the one that does the task best is kept.

| Maker | Parts | Used in |
|---|---|---|
| [Adafruit](adafruit) | BNO085 and BNO055 IMU breakouts | LeRobot humanoid (BNO055) |
| [Feetech](feetech) | STS3215 bus servo | SO-101, Open Duck Mini v2 |
| [RobStride](robstride) | RS00, RS02, RS03, RS05 actuators | LeRobot humanoid (all four) |
| [ROBOTIS](robotis) | DYNAMIXEL XL330, XC330, XL430, XC430, XM430, 2XL430, 2XC430 (ratings; mounting holes to come) | |
| [Raspberry Pi](raspberrypi) | Raspberry Pi 5, 4, Zero 2 W; Camera Module 3 | LeRobot humanoid (Pi 5), Open Duck Mini v2 (Zero 2 W) |
| [Waveshare](waveshare) | Bus Servo Adapter (A) driver board | SO-101 |

Standard parts that no single maker owns (bearings by their ISO sizes, heat-set inserts) are in the
framework, `yotown.gym.standard`.

## List your parts

Makers are welcome to add their own parts, and anyone may add a part they use. Open a pull request with
a folder `vendors/<maker>/`. A circuit board is a `yotown.gym.bought.Board` (outline, thickness,
mounting holes); other parts are a class of their own.

```text
vendors/<maker>/
  __init__.py      one class or instance per part (see feetech/ and robstride/)
  README.md        the parts, their sources, and links to buy them
  <part>.step      optional: your own CAD, if you publish it under a licence that allows it
```

Every part is held to the same rules, whoever adds it:

1. **A source for every number.** A datasheet, a drawing or a manual, linked in the README or beside
   the value. Where two sources differ, give both.
2. **The interfaces exactly.** Hole patterns, bores, shaft and horn dimensions, connector positions:
   whatever a printed part must fit. The rest of the outline can be simple.
3. **Facts, not marketing.** Dimensions, ratings, mass. Product names and a link to buy are fine;
   claims are not.
4. **Your own CAD only.** A STEP file goes in only from its maker, or under a licence that allows it.
5. **It builds.** `gym check` still passes for every robot.

## Template

```python
"""<Maker> <product line>.

Sources: <datasheet or drawing, with a link>.
"""

from __future__ import annotations

from dataclasses import dataclass

from yotown.gym.interfaces import BoltCircle, ScrewPattern


@dataclass(frozen=True)
class MyServo:
    """<Part>: what it is and which way its frame points."""

    length: float = 40.0                                          # mm, <source>
    horn: ScrewPattern = ScrewPattern(BoltCircle(14.0, 4, 45.0), "M2")   # <source>
    rated_nm: float = 1.0                                         # <source>
```
