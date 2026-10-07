"""Adafruit breakout boards.

Sources: Adafruit's published board layouts (EAGLE .brd) on GitHub, read 2026-10-06: the outline (the
Dimension layer) and the mounting holes (MOUNTINGHOLE_2.5_PLATED pads, drill 2.5):
  BNO085 (product 4754): github.com/adafruit/Adafruit-BNO08x-PCB, Adafruit_BNO08x.brd
  BNO055 STEMMA QT (product 4646): github.com/adafruit/Adafruit-BNO055-Breakout-PCB,
    "Adafruit BNO055 STEMMA QT.brd"
The holes sit 0.1 inch (2.54) in from each edge, centred on the board.
"""

from __future__ import annotations

from yotown.gym.bought import Board
from yotown.gym.interfaces import HoleGrid

BNO085 = Board("Adafruit BNO085 9-DOF IMU breakout (4754)", length=25.4, width=22.86,
               holes=HoleGrid((20.32, 17.78), 2.5), screw="M2.5")
BNO055 = Board("Adafruit BNO055 9-DOF IMU breakout, STEMMA QT (4646)", length=25.4, width=20.32,
               holes=HoleGrid((20.32, 15.24), 2.5), screw="M2.5")
