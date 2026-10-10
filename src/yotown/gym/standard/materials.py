"""Print materials by their density, and what a printed part weighs.

A part's material is solid only in its walls: inside them it is sparse infill. So a printed part weighs
less than its volume times its material's density, and how much less depends on its shape: a thin part
(a sheet, a blade) is nearly all wall and prints close to solid, a chunky one mostly infill.
`printed_mass` estimates it from the part's volume and surface area and how it is printed
(`PrintSettings`: the material, a solid skin `skin` mm deep over the whole surface, `infill` inside).
The defaults are a common print; a robot's shared.py sets its own once (`PRINT = PrintSettings(infill=0.2)`)
and a part that is printed differently (a sole in TPU, a solid bracket) passes its own.

The densities are typical values for the plastics, from filament makers' datasheets; a brand, a colour
or an additive moves them by a few percent. Your slicer reports a part's grams for your own settings,
and weighing a print is the best calibration of all.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Material:
    """A print material: its density as solid plastic (kg/m3), and the range makers list."""

    name: str
    density: float
    low: float
    high: float


PLA = Material("PLA", 1240.0, 1210.0, 1250.0)
PETG = Material("PETG", 1270.0, 1230.0, 1290.0)
ABS = Material("ABS", 1040.0, 1010.0, 1080.0)
TPU = Material("TPU", 1210.0, 1100.0, 1230.0)      # the flexible one (soles, bumpers): 95A and nearby
MATERIALS = {m.name: m for m in (PLA, PETG, ABS, TPU)}


@dataclass(frozen=True)
class PrintSettings:
    """How a part is printed, as far as its mass goes: the material, the solid skin's depth (mm: walls,
    top and bottom layers) and the infill (a fraction). The defaults are a common print."""

    material: Material = PLA
    skin: float = 0.8                               # two 0.4 mm perimeters, or top and bottom layers
    infill: float = 0.30


DEFAULT = PrintSettings()


def printed_fraction(volume_mm3: float, area_mm2: float, settings: PrintSettings = DEFAULT) -> float:
    """The part's mass as a fraction of solid: its skin (area x skin, at most the whole part) solid,
    the rest at the infill."""
    if volume_mm3 <= 0 or area_mm2 <= 0:
        return settings.infill
    shell = min(area_mm2 * settings.skin / volume_mm3, 1.0)
    return shell + (1.0 - shell) * settings.infill


def printed_mass(volume_mm3: float, area_mm2: float, settings: PrintSettings = DEFAULT) -> float:
    """A printed part's mass, kg, from its volume (mm3) and surface area (mm2), printed as `settings` says."""
    return settings.material.density * 1e-9 * volume_mm3 * printed_fraction(volume_mm3, area_mm2, settings)
