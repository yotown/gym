"""LeRobot humanoid knee rod, the other half: knee_rod12's program with HALF = -1 (y <= 0), the halves
one design -- an edit to the rod moves both."""

import os
import runpy


here = os.path.dirname(os.path.abspath(__file__))
# beside it in a part folder (<part>/written.py), or in a flat gym body (<part>.py)
ROD = next(p for p in (os.path.join(here, "..", "femur_v2_knee_rod12", "written.py"), os.path.join(here, "femur_v2_knee_rod12.py")) if os.path.exists(p))

result = runpy.run_path(ROD, init_globals={"HALF": -1})["result"]
