"""Open Duck Mini v2 antenna holder (right): the left holder's program, mirrored across the robot's middle
(y = 0).

Frame: the vendor's (mm)."""

import os
import runpy

here = os.path.dirname(os.path.abspath(__file__))
SOURCE = next(p for p in (os.path.join(here, "..", "left_antenna_holder", "written.py"), os.path.join(here, "left_antenna_holder.py")) if os.path.exists(p))
result = runpy.run_path(SOURCE)["result"].mirror("XZ")
