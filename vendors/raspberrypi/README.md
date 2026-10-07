# Raspberry Pi

Single-board computers and cameras. [raspberrypi.com](https://www.raspberrypi.com/)

| Part | Instance | Outline (mm) | Holes |
|---|---|---|---|
| Raspberry Pi 5 | `PI_5` | 85 x 56 | 58 x 49 apart, d2.7, M2.5 |
| Raspberry Pi 4 Model B | `PI_4` | 85 x 56 | 58 x 49 apart, d2.7, M2.5 |
| Raspberry Pi Zero 2 W | `PI_ZERO_2_W` | 65 x 30 | 58 x 23 apart, M2.5 |
| Camera Module 3 (standard and wide) | `CAMERA_MODULE_3`, `CAMERA_MODULE_3_WIDE` | 25 x 23.862 x 1.12 | 21 x 12.5 apart, d2.2 |

```python
from yotown.gym.vendors.raspberrypi import PI_5, CAMERA_MODULE_3

PI_5.hole_points()          # the four holes about the board's centre: they sit toward the GPIO end
CAMERA_MODULE_3.lens_at     # the lens, from the camera board's centre: a printed mount's window
```

A board's frame is its centre, its top face on z = 0, its length along x; the Pi 4 and Pi 5 have +x
toward their USB and Ethernet ports. A camera's lens faces +z.

The LeRobot humanoid carries a Raspberry Pi 5 in its torso; Open Duck Mini v2 a Zero 2 W in its head.

## Sources

Raspberry Pi Ltd's mechanical drawings and product briefs at
[datasheets.raspberrypi.com](https://datasheets.raspberrypi.com/):
[Raspberry Pi 5](https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf),
[Raspberry Pi 4](https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-mechanical-drawing.pdf),
[Zero 2 W](https://datasheets.raspberrypi.com/rpizero2/raspberry-pi-zero-2-w-mechanical-drawing.pdf)
(and the [Zero W's](https://datasheets.raspberrypi.com/rpizero/raspberry-pi-zero-w-mechanical-drawing.pdf),
the same outline, for "all holes M2.5"),
[Camera Module 3](https://datasheets.raspberrypi.com/camera/camera-module-3-product-brief.pdf)
(Physical specification).

Raspberry Pi gives these dimensions as approximate and for reference: check a printed part against a
real board.
