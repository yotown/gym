"""Waveshare boards.

Sources: Waveshare's wiki for the Bus Servo Adapter (A), https://www.waveshare.com/wiki/Bus_Servo_Adapter_(A):
its specification (42 x 33 mm, mounting holes d2.5) and its STEP model ("Bus Servo Adapter (A) STEP Model"
on that page), from which the board's thickness and the holes' positions are measured: 2.5 in from each
edge, so 37 x 28 between centres.
"""

from __future__ import annotations

from yotown.gym.bought import Board
from yotown.gym.interfaces import HoleGrid

BUS_SERVO_ADAPTER_A = Board("Bus Servo Adapter (A)", length=42.0, width=33.0, holes=HoleGrid((37.0, 28.0), 2.5),
                            thickness=1.6)
"""The serial bus servo driver board the SO-101 uses (Feetech STS/SCS servos)."""
