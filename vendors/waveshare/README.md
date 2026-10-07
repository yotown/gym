# Waveshare

Boards and servos for robots. [waveshare.com](https://www.waveshare.com/)

| Part | Instance | Used in |
|---|---|---|
| Bus Servo Adapter (A): serial bus servo driver board | `BUS_SERVO_ADAPTER_A` | SO-101 (`waveshare_plate`) |

```python
from yotown.gym.vendors.waveshare import BUS_SERVO_ADAPTER_A as BOARD

BOARD.length, BOARD.width, BOARD.thickness   # 42.0, 33.0, 1.6
BOARD.holes                                  # HoleGrid(pitch=(37.0, 28.0), hole_d=2.5)
```

The SO-101's `waveshare_plate` takes its four corner holes from `BOARD.holes.pitch`.

Waveshare also sells the Feetech STS3215 as the ST3215: see [feetech](../feetech).

## Sources

The [Bus Servo Adapter (A) wiki page](https://www.waveshare.com/wiki/Bus_Servo_Adapter_(A)): its
specification (42 x 33 mm, mounting holes d2.5), and its STEP model, from which the board's thickness
(1.6) and the holes' positions (2.5 in from each edge) are measured.
