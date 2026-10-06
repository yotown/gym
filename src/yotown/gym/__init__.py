"""Yo.Town Gym: robot parts as CadQuery programs.

    from yotown.gym import shared
    from yotown.gym.vendors.feetech import STS3215

A robot is a folder of part programs (robots/<robot>/parts/*.py) and a file of values its parts
share (robots/<robot>/shared.py), such as its servo, its screws and the dimensions where two parts
meet. A part reads them with `shared(__file__)`, so each shared value is written only once.
"""

from __future__ import annotations

import os
import runpy
from types import SimpleNamespace

__all__ = ["shared"]


def shared(part_file: str) -> SimpleNamespace:
    """Load the shared.py of the robot a part belongs to. It is looked for beside the part and one folder
    up (robots/<robot>/parts/<part>.py reads robots/<robot>/shared.py)."""
    here = os.path.dirname(os.path.abspath(part_file))
    for folder in (here, os.path.dirname(here)):
        path = os.path.join(folder, "shared.py")
        if os.path.exists(path):
            return SimpleNamespace(**{k: v for k, v in runpy.run_path(path).items() if not k.startswith("_")})
    raise FileNotFoundError("no shared.py beside %s or one folder up" % part_file)
