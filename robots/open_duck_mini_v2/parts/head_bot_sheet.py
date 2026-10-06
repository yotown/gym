"""Open Duck Mini v2 head bottom sheet, written from its STEP: interfaces exact, the body simple.

The head's floor: a plate tapering from its back to its front, its front sides drafted, open round the
neck (a countersunk opening on the yaw axis); eight screws up into the head, counterbored from below;
two holes through on the middle line.

Frame: the vendor's (mm); z up, symmetric about y = 0.
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
# the sheet fills the head's rim: its outline is the head cavity's at the rim, its top the rim bosses' feet
TOP_Z = 112.71                             # its top, under the head's rim bosses
BACK_X = -76.9                             # the back edge,
BACK_HALF_W = 51.65                        # half its width there
FRONT_X = 116.9                            # the front edge,
FRONT_HALF_W = 95.81                       # half its width there
TAPER_TO_X = 80.1                          # the sides taper out to here, then run straight  # measured
SCREWS = [(105.0, 69.0), (80.0, 84.0), (4.061, 62.06), (-68.391, 44.501)]   # up into the head's rim, each and its mirror in y
SCREW_D = 3.2
SCREW_HEAD_D = 6.5
SCREW_HEAD_SEAT = 1.0                      # above the underside
THROUGH = [((-59.5, 0.0), 5.0), ((-44.5, 0.0), 15.0)]   # the cables' holes through: (x, y), d
OPENING_X = 20.0                           # the opening round the neck, on the yaw axis,
OPENING_BOTTOM_R = 45.0                    # countersunk: r at the bottom,
OPENING_TOP_R = 55.0                       # at the top
SIDE_DRAFT_DEG = 20.0                      # the straight sides lean in towards the top, as the head cavity's wall does

# -- body: free -------------------------------------------------------------------------------------

half = [(BACK_X, BACK_HALF_W), (TAPER_TO_X, FRONT_HALF_W), (FRONT_X, FRONT_HALF_W)]
outline = half + [(x, -y) for x, y in reversed(half)]
sheet = cq.Workplane("XY", origin=(0, 0, S.HEAD_RIM_Z)).polyline(outline).close().extrude(TOP_Z - S.HEAD_RIM_Z)
lean = (TOP_Z - S.HEAD_RIM_Z) * math.tan(math.radians(SIDE_DRAFT_DEG))
fh = FRONT_HALF_W
for s in (1, -1):                          # the straight sides' draft: a wedge off each top edge
    wedge = cq.Workplane("YZ", origin=(TAPER_TO_X, 0, 0)).polyline([(s * fh, S.HEAD_RIM_Z), (s * (fh + 1), S.HEAD_RIM_Z), (s * (fh + 1), TOP_Z), (s * (fh - lean), TOP_Z)]).close() \
        .extrude(FRONT_X - TAPER_TO_X + 1)
    sheet = sheet.cut(wedge)
below = cq.Workplane("XY", origin=(0, 0, S.HEAD_RIM_Z - 1))
for at, d in THROUGH:
    sheet = sheet.cut(below.center(*at).circle(d / 2).extrude(TOP_Z - S.HEAD_RIM_Z + 2))
sheet = sheet.cut(cq.Workplane().add(cq.Solid.makeCone(OPENING_BOTTOM_R, OPENING_TOP_R, TOP_Z - S.HEAD_RIM_Z, cq.Vector(OPENING_X, 0, S.HEAD_RIM_Z))))

# -- interfaces, cut last -------------------------------------------------------------------------
pts = [(x, s * y) for x, y in SCREWS for s in (1, -1)]
sheet = sheet.cut(below.pushPoints(pts).circle(SCREW_D / 2).extrude(TOP_Z - S.HEAD_RIM_Z + 2)).cut(below.pushPoints(pts).circle(SCREW_HEAD_D / 2).extrude(SCREW_HEAD_SEAT + 1))

result = sheet
