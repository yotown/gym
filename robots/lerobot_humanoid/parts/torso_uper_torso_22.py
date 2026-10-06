"""LeRobot humanoid upper torso, the -x half of the shoulder bar: torso_upper_torso_12's program mirrored across
the split face. It has no tab on the outside and no bores across; its bolts to the other half are M4
clearance, and its two small holes go down through the floor.

Frame: the vendor's (the torso's STEP frame, mm), as torso_upper_torso_12's."""

import os
import runpy

here = os.path.dirname(os.path.abspath(__file__))
SOURCE = next(p for p in (os.path.join(here, "..", "torso_upper_torso_12", "written.py"), os.path.join(here, "torso_upper_torso_12.py"))
              if os.path.exists(p))
HALF = dict(mirror=True, middle_tab=False, bores=False,
            bolt_d=4.3,                    # M4 clearance
            tab_holes_x=19.91)             # mirrored: x -18.99 on this half  # measured
result = runpy.run_path(SOURCE, init_globals={"HALF": HALF})["result"]
