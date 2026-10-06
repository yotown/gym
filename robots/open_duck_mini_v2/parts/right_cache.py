"""Open Duck Mini v2 leg cover (the right leg's "cache"): the left cover's program, mirrored across the
robot's middle (y = 0).

Frame: the vendor's (mm)."""

import os
import runpy

here = os.path.dirname(os.path.abspath(__file__))
SOURCE = next(p for p in (os.path.join(here, "..", "left_cache", "written.py"), os.path.join(here, "left_cache.py")) if os.path.exists(p))
result = runpy.run_path(SOURCE)["result"].mirror("XZ")
