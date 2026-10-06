"""Open Duck Mini v2 knee-to-ankle sheet (the inner one): the servo sheet's program (left_knee_to_ankle_left_sheet)
with its differences. A thinner plate and a shallower block; the ankle servo's screws nearer the horn,
their heads less deep; a wider, deeper step in the case's pocket and a slot for the servo's cable.

Frame: the vendor's (mm); in the sheet's own frame as the program says."""

import os
import runpy

here = os.path.dirname(os.path.abspath(__file__))
SOURCE = next(p for p in (os.path.join(here, "..", "left_knee_to_ankle_left_sheet", "written.py"),
                          os.path.join(here, "left_knee_to_ankle_left_sheet.py")) if os.path.exists(p))
SHEET = dict(thick=3.85, servo_seat_w=-1.95,
             servo_back=32.55, servo_head_w=0.05, horn_head_w=2.85, rod_head_w=1.85,
             step_w=18.48, step_back=29.75, step_deep=1.9,   # measured
             cable_w=10.0, cable_back=38.11, cable_top_w=2.95, cable_end_r=3.0, cable_end_w=-0.05)
PLACE = dict(origin=(-16.06, 72.05, -143.65), v=(0, 0, -1), w=(0, -1, 0))   # its outer face looks out of the leg the other way
result = runpy.run_path(SOURCE, init_globals={"SHEET": SHEET, "PLACE": PLACE})["result"]
