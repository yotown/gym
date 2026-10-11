"""Flamingo neck sheet (the right one): the Duck's neck_right_sheet program, its link the Flamingo's NECK.

Frame: the Duck's (mm), as that program's.
"""

import runpy

from yotown.gym import shared

S = shared(__file__)
result = runpy.run_path(S.duck("neck_right_sheet"), init_globals={"LINK": S.NECK})["result"]
