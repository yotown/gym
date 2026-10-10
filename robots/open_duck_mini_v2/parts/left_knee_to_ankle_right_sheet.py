"""Open Duck Mini v2 knee-to-ankle sheet (the inner one): the servo sheet's program (left_knee_to_ankle_left_sheet)
with its differences. It sits on the servos' idler side: the horn servo's idler, the next servo's case's
other face (its seat, step and screws are that face's). A thinner plate, a slot for the servo's cable.

Frame: the vendor's (mm); in the sheet's own frame as the program says."""

import os
import runpy

here = os.path.dirname(os.path.abspath(__file__))
SOURCE = next(p for p in (os.path.join(here, "..", "left_knee_to_ankle_left_sheet", "written.py"),
                          os.path.join(here, "left_knee_to_ankle_left_sheet.py")) if os.path.exists(p))
SHEET = dict(side="idler", thick=3.85, servo_grip=2.0, horn_head_w=2.85, rod_head_w=1.85,
             cable_w=10.0, cable_top_w=2.95, cable_end_r=3.0)
result = runpy.run_path(SOURCE, init_globals={"SHEET": SHEET})["result"]
