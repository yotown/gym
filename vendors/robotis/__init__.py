"""ROBOTIS DYNAMIXEL X-series servos.

Sources: the ROBOTIS e-manual page of each model, https://emanual.robotis.com/docs/en/dxl/x/<model>/
(for example .../xc430-w240/), its Specifications table, read 2026-10-06.

ROBOTIS publishes STALL torque: what the servo gives with its shaft held still, at its stall current. It
is not a torque to hold continuously; plan a joint's continuous load well below it.

Not included yet: the case's mounting holes and the horn's pattern. They are in ROBOTIS's drawings
(the Drawings section of each page), which are to be read before a printed part depends on them.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Dynamixel:
    """A DYNAMIXEL servo: its case (W x H x D as ROBOTIS gives it), mass, gearing, and its stall torque
    and no-load speed at each voltage ROBOTIS lists."""

    name: str
    width: float                    # mm
    height: float
    depth: float
    mass_g: float
    gear_ratio: float
    volts: tuple                    # (min, max) input voltage
    stall: tuple                    # ((N m, at V, at A), ...)
    no_load_rpm: tuple              # ((rev/min, at V), ...)
    axes: int = 1                   # 2: two servos in one case (2XL430, 2XC430)

    def stall_nm(self, volts: float) -> float:
        """The stall torque at the listed voltage closest to `volts`."""
        return min(self.stall, key=lambda s: abs(s[1] - volts))[0]


XL330_M077 = Dynamixel("XL330-M077-T", 20.0, 34.0, 26.0, 18, 77.5, (3.7, 6.0),
                       ((0.180, 3.7, 1.11), (0.215, 5.0, 1.47), (0.228, 6.0, 1.74)),
                       ((278, 3.7), (383, 5.0), (456, 6.0)))
XL330_M288 = Dynamixel("XL330-M288-T", 20.0, 34.0, 26.0, 18, 288.4, (3.7, 6.0),
                       ((0.42, 3.7, 1.11), (0.52, 5.0, 1.47), (0.60, 6.0, 1.74)),
                       ((76, 3.7), (103, 5.0), (123, 6.0)))
XC330_T288 = Dynamixel("XC330-T288-T", 20.0, 34.0, 26.0, 23, 288.35, (6.5, 12.0),
                       ((0.76, 9.0, 0.61), (0.92, 11.1, 0.80), (1.00, 12.0, 0.88)),
                       ((52, 9.0), (65, 11.1), (71, 12.0)))
XL430_W250 = Dynamixel("XL430-W250-T", 28.5, 46.5, 34.0, 57.2, 258.5, (6.5, 12.0),
                       ((1.0, 9.0, 1.0), (1.4, 11.1, 1.3), (1.5, 12.0, 1.4)),
                       ((47, 9.0), (57, 11.1), (61, 12.0)))
XC430_W240 = Dynamixel("XC430-W240-T", 28.5, 46.5, 34.0, 65, 245.22, (6.5, 14.8),
                       ((1.4, 9.0, 1.1), (1.7, 11.1, 1.3), (1.9, 12.0, 1.4)),
                       ((52, 9.0), (65, 11.1), (70, 12.0)))
XM430_W210 = Dynamixel("XM430-W210-T", 28.5, 46.5, 34.0, 82, 212.6, (10.0, 14.8),
                       ((2.7, 11.1, 2.1), (3.0, 12.0, 2.3), (3.7, 14.8, 2.7)),
                       ((70, 11.1), (77, 12.0), (95, 14.8)))
XM430_W350 = Dynamixel("XM430-W350-T", 28.5, 46.5, 34.0, 82, 353.5, (10.0, 14.8),
                       ((3.8, 11.1, 2.1), (4.1, 12.0, 2.3), (4.8, 14.8, 2.7)),
                       ((43, 11.1), (46, 12.0), (57, 14.8)))
XL430_W250_2X = Dynamixel("2XL430-W250-T", 36.0, 46.5, 36.0, 98.2, 257.4, (6.5, 12.0),
                          ((1.0, 9.0, 1.0), (1.4, 11.1, 1.3), (1.5, 12.0, 1.4)),
                          ((47, 9.0), (57, 11.1), (61, 12.0)), axes=2)
XC430_W250_2X = Dynamixel("2XC430-W250-T", 36.0, 46.5, 36.0, 102, 257.4, (6.5, 14.8),
                          ((1.3, 9.0, 1.1), (1.6, 11.1, 1.3), (1.8, 12.0, 1.4)),
                          ((48, 9.0), (59, 11.1), (64, 12.0)), axes=2)

ALL = (XL330_M077, XL330_M288, XC330_T288, XL430_W250, XC430_W240, XM430_W210, XM430_W350,
       XL430_W250_2X, XC430_W250_2X)
