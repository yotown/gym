"""Ball bearings by their standard sizes (ISO 15 / 355 dimension series): bore, outside diameter, width."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Bearing:
    """A ball bearing: bore, outside diameter and width (mm)."""

    bore: float
    od: float
    width: float
    name: str = ""


B625 = Bearing(5.0, 16.0, 5.0, "625")
B6702 = Bearing(15.0, 21.0, 4.0, "6702")       # thin section (61702)
B6207 = Bearing(35.0, 72.0, 17.0, "6207")
