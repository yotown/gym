"""Base types for bought parts that are not standard sizes: what a printed part needs to hold one.

A maker's part in vendors/<maker>/ is an instance of one of these, or a class of its own when its
features do not fit one (an actuator's faces, a servo's horn).
"""

from __future__ import annotations

from dataclasses import dataclass

from yotown.gym.interfaces import HoleGrid


@dataclass(frozen=True)
class Board:
    """A circuit board: its outline, its mounting holes, and its thickness when the maker gives it.

    Frame: the board's centre, its top face on z = 0, its length along x (mm). Components stand on the
    top face; a printed part that carries the board uses the holes and clears the outline. The holes'
    pattern is centred at `holes_at` (x, y) from the board's centre: (0, 0) when the board is symmetric
    about its holes, as many are not."""

    name: str
    length: float                   # along x
    width: float                    # along y
    holes: HoleGrid
    holes_at: tuple = (0.0, 0.0)    # the hole pattern's centre, from the board's centre
    screw: str = ""                 # the screw the holes take, as the maker names it ("M2.5")
    thickness: float | None = None  # the circuit board alone, without its components
    mass_g: float | None = None

    def hole_points(self) -> list:
        """The holes' centres in the board's frame: [(x, y), ...]."""
        return self.holes.points(self.holes_at)
