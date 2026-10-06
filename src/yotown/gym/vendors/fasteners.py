"""Fasteners: the holes a printed part needs for them."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HeatSetInsert:
    """A threaded brass insert, pressed into a printed hole with a soldering iron: the hole diameter
    and depth it needs."""

    hole_d: float
    depth: float
    thread: str = ""                # "M3", ...
