"""Types for the dimensions where two parts meet: a bolt circle, a screw's hole and head, a tapped
pattern, locating pins, a grid of holes on a rectangle.

Both parts use the same value, so editing it changes both. Values cannot be modified; a variant is a new
value, for example `horn.rotated(-2.8)`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class BoltCircle:
    """Equal holes on a circle: its diameter, how many, and the first one's angle from the plane's x."""

    d: float
    count: int
    first_deg: float = 0.0

    def on(self, wp):
        """The holes' centres on a workplane (about its origin): then `.circle(...)`, `.hole(...)`."""
        return wp.polarArray(self.d / 2, self.first_deg, 360, self.count)

    def points(self, at: tuple = (0.0, 0.0)) -> list:
        """The holes' centres about a point, in a plane: [(x, y), ...], the first at first_deg."""
        cx, cy = at
        out = []
        for i in range(self.count):
            a = math.radians(self.first_deg + 360.0 * i / self.count)
            out.append((cx + round(self.d / 2 * math.cos(a), 12), cy + round(self.d / 2 * math.sin(a), 12)))
        return out

    def rotated(self, deg: float) -> "BoltCircle":
        """The same bolt circle, turned by deg."""
        return replace(self, first_deg=self.first_deg + deg)


@dataclass(frozen=True)
class Screw:
    """A screw in a printed part: the hole it goes through, the counterbore for its head, and the
    thickness it clamps under the head (between the counterbore's floor and the mating face)."""

    hole_d: float
    head_d: float
    grip: float = 0.0


@dataclass(frozen=True)
class ScrewPattern:
    """Tapped holes in a bought part, on a bolt circle: the thread a printed part's screws take, and how
    deep the thread goes (a screw longer than the part's grip plus this bottoms out)."""

    circle: BoltCircle
    thread: str
    depth: float = 0.0


@dataclass(frozen=True)
class PinPattern:
    """Locating pins (or holes for them) on a bolt circle: the pins' diameter."""

    circle: BoltCircle
    pin_d: float


@dataclass(frozen=True)
class HoleGrid:
    """Holes on the corners of a rectangle, about its centre: the spacing along x and y, and the holes'
    diameter. A board's mounting holes, a plate's corner screws."""

    pitch: tuple
    hole_d: float | None = None     # None where the source names only the screw

    def on(self, wp):
        """The holes' centres on a workplane (about its origin): then `.circle(...)`, `.hole(...)`."""
        return wp.rarray(self.pitch[0], self.pitch[1], 2, 2)

    def points(self, at: tuple = (0.0, 0.0)) -> list:
        """The holes' centres about a point, in a plane: [(x, y), ...]."""
        cx, cy = at
        hx, hy = self.pitch[0] / 2, self.pitch[1] / 2
        return [(round(cx + sx * hx, 12), round(cy + sy * hy, 12)) for sy in (-1, 1) for sx in (-1, 1)]
