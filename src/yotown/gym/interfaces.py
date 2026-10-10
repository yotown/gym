"""Types for the dimensions where two parts meet: a bolt circle, a screw's hole and head, a tapped
pattern, locating pins, a grid of holes on a rectangle, a servo's faces as the plates on it see them.

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


@dataclass(frozen=True)
class CaseFace:
    """One of a servo's two faces across its output axis, as a plate screwed to it sees it (in the
    servo's axis frame: see ServoFaces)."""

    level: float                    # the face the plate bears on: its distance from the horn's face, along the axis
    screws: tuple                   # its screw holes (tapped, or through its tabs): (back, across) each
    thread: str
    boss: tuple | None = None       # a raised part of the face, standing proud past `level`: (wide across, from back, proud)


@dataclass(frozen=True)
class ServoFaces:
    """A servo as the plates screwed across its output axis see it: a plate on its horn (or its idler),
    a plate on each face of its case. The two horns and the two faces make a sandwich, and a link of two
    plates spans from one servo's horns to the next servo's case.

    Frame (mm): the origin on the output axis, at the horn's outer face (the face a plate bears on); `z` along the axis into the
    servo, towards the idler; `back` along the case's length, from the axis to the case's far end;
    `across` its width. A bolt circle's first angle is from `back`.
    """

    horn: BoltCircle                # the horn's holes a plate screws to
    horn_thread: str
    hub_d: float                    # the horn's hub (a plate on the horn clears it),
    hub_proud: float                # standing this far out of the horn's face
    idler_face: float               # the idler's outer face (the other horn): its distance along the axis
    idler: BoltCircle
    idler_hub_d: float
    idler_hub_proud: float          # out of the idler's face, away from the servo
    case_near: float                # the case's near end, from the axis (away from back)
    case_back: float                # its far end, back from the axis
    case_width: float
    horn_side: CaseFace             # the case's face on the horn's side
    idler_side: CaseFace            # and on the idler's

    def side(self, which: str) -> CaseFace:
        """The case's face on "horn" or "idler" side."""
        return {"horn": self.horn_side, "idler": self.idler_side}[which]
