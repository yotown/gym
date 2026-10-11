"""Flamingo shin sheet (the inner one): the Duck's left_knee_to_ankle_right_sheet program, its link the Flamingo's SHIN.

Frame: the Duck's (mm), as that program's.
"""

import runpy

from yotown.gym import shared

S = shared(__file__)
result = runpy.run_path(S.duck("left_knee_to_ankle_right_sheet"), init_globals={"SHEET": {"link": S.SHIN}})["result"]
