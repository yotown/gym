"""Raspberry Pi boards and cameras.

Sources: Raspberry Pi Ltd's mechanical drawings and product briefs, https://datasheets.raspberrypi.com/
(read 2026-10-06):
  Raspberry Pi 5: rpi5/raspberry-pi-5-mechanical-drawing.pdf
  Raspberry Pi 4 Model B: rpi4/raspberry-pi-4-mechanical-drawing.pdf
  Raspberry Pi Zero 2 W: rpizero2/raspberry-pi-zero-2-w-mechanical-drawing.pdf, and the Zero W's drawing
    (rpizero/raspberry-pi-zero-w-mechanical-drawing.pdf, the same outline and holes) for "all holes M2.5"
  Camera Module 3: camera/camera-module-3-product-brief.pdf, Physical specification

Raspberry Pi notes that its drawings' dimensions are approximate and for reference; check a part against
a physical board before production.
"""

from __future__ import annotations

from dataclasses import dataclass

from yotown.gym.bought import Board
from yotown.gym.interfaces import HoleGrid

# Raspberry Pi 4 and 5: 85 x 56, holes 58 x 49 apart, 3.5 in from the GPIO end and from each long edge.
# x toward the USB and Ethernet end, so the holes' centre is 10 back from the board's.
PI_5 = Board("Raspberry Pi 5", length=85.0, width=56.0, holes=HoleGrid((58.0, 49.0), 2.7), holes_at=(-10.0, 0.0),
             screw="M2.5")
PI_4 = Board("Raspberry Pi 4 Model B", length=85.0, width=56.0, holes=HoleGrid((58.0, 49.0), 2.7),
             holes_at=(-10.0, 0.0), screw="M2.5")
# Raspberry Pi Zero 2 W: 65 x 30, holes 58 x 23 apart, 3.5 in from every edge. The drawing gives the
# screw, not the holes' diameter.
PI_ZERO_2_W = Board("Raspberry Pi Zero 2 W", length=65.0, width=30.0, holes=HoleGrid((58.0, 23.0)), screw="M2.5")


@dataclass(frozen=True)
class Camera:
    """A camera module: its board, and where its lens is.

    Frame: the board's (see Board): x across the board, y toward the lens's side of the board, the lens
    facing +z."""

    board: Board
    lens_at: tuple                  # the lens's axis, from the board's centre (x, y)
    lens_d: float                   # the lens barrel's diameter
    height: float                   # the board's back to the lens's front


# Camera Module 3: a 25 x 23.862 board, 1.12 thick; holes d2.2, 2.0 in from each side (21 apart) and at
# 2.0 and 14.5 up from the bottom edge (12.5 apart); the lens centred across, 14.4 up. The holes' centre is
# 8.25 up, 3.681 below the board's centre; the lens 2.469 above it.
_CAMERA_3_BOARD = Board("Camera Module 3", length=25.0, width=23.862, holes=HoleGrid((21.0, 12.5), 2.2),
                        holes_at=(0.0, -3.681), thickness=1.12)
CAMERA_MODULE_3 = Camera(_CAMERA_3_BOARD, lens_at=(0.0, 2.469), lens_d=5.75, height=11.5)
CAMERA_MODULE_3_WIDE = Camera(_CAMERA_3_BOARD, lens_at=(0.0, 2.469), lens_d=6.95, height=12.4)
