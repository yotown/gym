"""LeRobot humanoid tibia, the other leg's (tibias 12): tibias22's program mirrored about y 19, with
this part's holes -- one design, so an edit to the tibia's body moves both.

The actuator mounts from the other side: its 8-screw ring and the key bar change pockets. The back
plate's grid is counterbored; the ankle's seat is stepped, with three screws; the lobe's front hole
is counterbored. Each value is in tibias22's frame (y' = 38 - y), before the mirror."""

import os
import runpy

TIBIA = dict(
    mirror_about_y=19.0,
    motor_pocket={(0.0, 154.0): (46.0, 38.0, 41.5), (0.0, 207.0): (46.0, 32.3, 41.0)},
    key_at=(0.0, 154.0),
    m3_ring={(0.0, 207.0): (41.5, 22.5, 8, 41.0), (0.0, 154.0): (38.5, 53.0, 4, 41.5)},
    ankle_seat=((19.0, 37.0, 39.0), (21.0, 39.0, 43.0)),
    ankle_screws=(2.3, 25.0, 30.0, 3),
    back_holes=((4.2, 19.0, 21.0), (7.8, 21.0, 29.0)),
    lobe_seat=((21.0, 31.0, 35.0), (19.0, 35.0, 38.0), (3.5, 38.0, 40.0), (6.5, 40.0, 43.0)),
)

here = os.path.dirname(os.path.abspath(__file__))
# beside it in a part folder (<part>/written.py), or in a flat gym body (<part>.py)
TIBIAS22 = next(p for p in (os.path.join(here, "..", "tibias2_tibias22", "written.py"), os.path.join(here, "tibias2_tibias22.py")) if os.path.exists(p))
result = runpy.run_path(TIBIAS22, init_globals={"TIBIA": TIBIA})["result"]
