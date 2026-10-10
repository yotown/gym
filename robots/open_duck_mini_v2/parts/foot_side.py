"""Open Duck Mini v2 foot (the side half): foot_top's program with its differences, mirrored across the foot.
The same outline, plate and horn mount (the ankle's other side); a shorter tray, no windows and no lip
for the sole; the pins' holes counterbored from outside.

Frame: the vendor's (mm); before the mirror, in foot_top's (its outer face onto foot_top's)."""

import os
import runpy

here = os.path.dirname(os.path.abspath(__file__))
SOURCE = next(p for p in (os.path.join(here, "..", "foot_top", "written.py"), os.path.join(here, "foot_top.py")) if os.path.exists(p))
FOOT = dict(side="idler", sole_lip=None, windows=None)   # its plate on the ankle servo's idler, mirrored onto it
result = runpy.run_path(SOURCE, init_globals={"FOOT": FOOT})["result"]
