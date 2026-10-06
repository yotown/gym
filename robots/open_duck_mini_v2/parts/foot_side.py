"""Open Duck Mini v2 foot (the side half): foot_top's program with its differences, mirrored across the foot.
The same outline, plate and horn mount (the ankle's other side); a shorter tray, no windows and no lip
for the sole; the pins' holes counterbored from outside.

Frame: the vendor's (mm); before the mirror, in foot_top's (its outer face onto foot_top's)."""

import os
import runpy

here = os.path.dirname(os.path.abspath(__file__))
SOURCE = next(p for p in (os.path.join(here, "..", "foot_top", "written.py"), os.path.join(here, "foot_top.py")) if os.path.exists(p))
FOOT = dict(back=102.05, pocket_to=105.55, sole_lip=None, windows=None,
            pin_holes=[(3.5, 102.05, 108.05), (6.5, 108.05, 114.05)],
            foot_edge=((102.05, -245.758), 12.0),             # measured
            mirror_about_y=90.6)                              # foot_top's outer face (114.05) onto foot_side's (67.15)
result = runpy.run_path(SOURCE, init_globals={"FOOT": FOOT})["result"]
