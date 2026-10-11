"""Flamingo right leg cover: the Duck's left_cache program, over the knee of the Flamingo's THIGH, mirrored across the robot's middle (y = 0).

Frame: the Duck's (mm), as that program's.
"""

import runpy

from yotown.gym import shared

S = shared(__file__)
result = runpy.run_path(S.duck("left_cache"), init_globals={"LINK": S.THIGH})["result"].mirror("XZ")
