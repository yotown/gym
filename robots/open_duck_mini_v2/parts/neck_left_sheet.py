"""Open Duck Mini v2 neck sheet (the left one): the servo sheet's program (left_knee_to_ankle_left_sheet) with
its differences. The neck pitch servo's horn below, the head's pitch servo screwed to the block above;
a shorter sheet, thicker, its sides leaning more; no rods through it; a smaller pocket for the case.

Frame: the vendor's (mm); in the sheet's own frame as the program says."""

import os
import runpy

here = os.path.dirname(os.path.abspath(__file__))
SOURCE = next(p for p in (os.path.join(here, "..", "left_knee_to_ankle_left_sheet", "written.py"),
                          os.path.join(here, "left_knee_to_ankle_left_sheet.py")) if os.path.exists(p))
SHEET = dict(link=66.0, thick=4.0, foot_w=30.72,
             lean_from_v=30.89, lean_deg=7.85,                # measured
             block_back=54.11, servo_seat_w=-1.95, pocket_w=14.2, pocket_back=35.11, rim=1.1, step=None,
             rods=None, servo_head_w=0.0,
             horn_head_w=2.0, inner_bore_deep=1.5)
PLACE = dict(origin=(20.0, 19.05, 25.11), v=(0, 0, 1), w=(0, 1, 0))
result = runpy.run_path(SOURCE, init_globals={"SHEET": SHEET, "PLACE": PLACE})["result"]
