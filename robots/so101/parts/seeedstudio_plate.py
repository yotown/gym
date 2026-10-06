"""SO-101 Seeed Studio mounting plate, written from its STEP: the servo-driver board's plate.

The Waveshare plate's blank (waveshare_plate: a 51 x 42 plate, 4 thick, and the dovetailed square tenon
on top that slides into the base), with this board's four counterbored screw holes on the +x side.
Frame: the vendor's STEP (mm), as waveshare_plate's: the plate lies on z = 0, its centre on the z axis.
"""

import os
import runpy

import cadquery as cq

here = os.path.dirname(os.path.abspath(__file__))
SOURCE = next(p for p in (os.path.join(here, "..", "waveshare_plate", "written.py"),
                          os.path.join(here, "waveshare_plate.py")) if os.path.exists(p))

# -- interfaces -- fixed ----------------------------------------------------------------------------
BOARD_AT_X = 14.617                        # the board's hole pattern centre  # measured
HOLE_PITCH = (16.5, 21.0)                  # x, y
HOLE_D = 2.1
CBORE_D = 3.6                              # counterbored from the top,
CBORE_DEPTH = 2.0                          # this deep
TENON_FLARE = 1.159                        # the tenon's flare each side; not in the model: this part (the dovetail as the Waveshare plate's)  # measured
TENON_FLARE_H = 1.2                        # over this height; not in the model: this part (the dovetail as the Waveshare plate's)  # measured

# -- body: free -------------------------------------------------------------------------------------

plate = runpy.run_path(SOURCE, init_globals={"PLATE": {"tenon_flare": TENON_FLARE, "tenon_flare_h": TENON_FLARE_H}})
blank, top, bottom = plate["blank"], plate["PLATE_TOP_Z"], plate["bottom"]

# -- interfaces, cut last -------------------------------------------------------------------------
holes = cq.Workplane("XY", origin=(BOARD_AT_X, 0, bottom - 1)).rarray(*HOLE_PITCH, 2, 2)
blank = blank.cut(holes.circle(HOLE_D / 2).extrude(top - bottom + 2))
heads = cq.Workplane("XY", origin=(BOARD_AT_X, 0, top - CBORE_DEPTH)).rarray(*HOLE_PITCH, 2, 2)
result = blank.cut(heads.circle(CBORE_D / 2).extrude(CBORE_DEPTH + 1))
