"""LeRobot humanoid shin spacer, written from its STEP: a bar across the shin, its ends rounded, two
screws through it along y. Frame: the STEP's (mm)."""

import cadquery as cq

# -- interfaces -- fixed ----------------------------------------------------------------------------
AT_Z = 180.5                               # its middle plane
SCREWS = [(-17.5, 3.8), (17.5, 4.1)]       # (x, diameter), along y  # measured

# -- body: free -------------------------------------------------------------------------------------
DEPTH = 37.0                               # across the shin (y from 0)
LENGTH = 43.0                              # along x
THICKNESS = 6.0                            # along z
END_R = 2.0                                # its four long edges

bar = (cq.Workplane("XY").box(LENGTH, DEPTH, THICKNESS).translate((0, DEPTH / 2, AT_Z))
       .edges("|Y").fillet(END_R))

# -- interfaces, cut last -------------------------------------------------------------------------
for x, d in SCREWS:
    bar = bar.cut(cq.Workplane("XZ", origin=(0, DEPTH, 0)).center(x, AT_Z).circle(d / 2).extrude(DEPTH))
result = bar
