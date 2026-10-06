"""Open Duck Mini v2 neck sheet (the right one): the servo sheet's program (left_knee_to_ankle_left_sheet) with
its differences, as the left neck sheet's but facing the other way: a shallower block, a wider pocket for
the head pitch servo's case, its screws nearer the horn, and a slot for the servo's cable.

Frame: the vendor's (mm); in the sheet's own frame as the program says."""

import os
import runpy

here = os.path.dirname(os.path.abspath(__file__))
SOURCE = next(p for p in (os.path.join(here, "..", "left_knee_to_ankle_left_sheet", "written.py"),
                          os.path.join(here, "left_knee_to_ankle_left_sheet.py")) if os.path.exists(p))
SHEET = dict(link=66.0, thick=4.05, foot_w=30.72,
             lean_from_v=30.89, lean_deg=7.85,                # measured
             block_back=54.11, servo_seat_w=0.1, pocket_w=18.68, pocket_back=29.75, rim=1.9, step=None,   # measured
             rods=None, servo_back=32.75, servo_head_w=0.05,
             cable_w=10.0, cable_back=35.11, cable_top_w=2.1, cable_end_r=5.0, cable_end_w=-2.9,
             horn_head_w=2.05, inner_bore_deep=1.5)
PLACE = dict(origin=(20.0, -17.8, 25.11), v=(0, 0, 1), w=(0, -1, 0))
result = runpy.run_path(SOURCE, init_globals={"SHEET": SHEET, "PLACE": PLACE})["result"]
