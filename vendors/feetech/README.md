# Feetech

Bus servos. [feetechrc.com](https://www.feetechrc.com/)

| Part | Class | Used in |
|---|---|---|
| STS3215 bus servo (sold by Waveshare as the ST3215) | `STS3215` | SO-101, Open Duck Mini v2 |

```python
from yotown.gym.vendors.feetech import STS3215

servo = STS3215()
servo.horn          # the horn's four holes: BoltCircle(14.0, 4, 45.0)
```

## Sources

- Feetech's STS3215 2D drawing, as Waveshare publishes it for the ST3215:
  [ST3215-2D.zip](https://files.waveshare.com/upload/0/08/ST3215-2D.zip)
- The STS3215 STEP in TheRobotStudio's [SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100)
  (Apache-2.0)

Where the drawing and the STEP differ, the class gives both.
