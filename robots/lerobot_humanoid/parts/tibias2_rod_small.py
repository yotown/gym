"""LeRobot humanoid tibia rod (the small one): the long rod's program with this rod's dimensions --
one design, so an edit to the rod's section or tabs moves both."""

import os
import runpy


ROD = dict(pin_at=(0.0, 24.0), pin_pitch=95.0,   # the pins along z (x, y); pin to pin
           heel=(-1, 1),                          # the heel's corner from the pin: towards -x, +y
           side=(14.0, 15.0), leg=(4.0, 5.0))     # measured

here = os.path.dirname(os.path.abspath(__file__))
# beside it in a part folder (<part>/written.py), or in a flat gym body (<part>.py)
LONG = next(p for p in (os.path.join(here, "..", "tibias2_rod_long", "written.py"), os.path.join(here, "tibias2_rod_long.py")) if os.path.exists(p))
result = runpy.run_path(LONG, init_globals={"ROD": ROD})["result"]
