"""Open Duck Mini v2 sole pad (TPU), written from its STEP: interfaces exact, the body simple.

A pad under the foot: its top the foot's sole, its tread a smaller rectangle below; between them each
side runs down in a straight flank and turns round an R8 onto the tread. Two screws up into the sole
insert (foot_bottom_pla), counterbored from below.

Frame: the vendor's (mm): the foot's, z up.
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
TOP = -253.625                             # the foot's sole: the pad's top on it
SCREW_D = 3.4
SCREW_HEAD_D = 6.5
SCREW_HEAD_SEAT = 3.0                      # below the top

# -- body: free -------------------------------------------------------------------------------------
THICK = 8.0
FOOTPRINT_X = (-54.15, 47.78)              # its top: x,  # measured
FOOTPRINT_Y = (70.09, 110.82)              # y  # measured
TREAD_X = (-43.786, 39.85)                 # the R8 rounds' centres, at the top's level: x,  # measured
TREAD_Y = (82.746, 97.444)                 # y  # measured
ROUND_R = 8.0


def side_profile(top_from, top_to, c_from, c_to):
    """A section across the pad: the top from top_from to top_to, each flank tangent to an R8 about c (at TOP)."""
    def tangent(p, c, s):                  # the point on the circle about (c, TOP) touched by the line from (p, TOP)
        dist = abs(p - c)
        if dist <= ROUND_R:                # the top ends inside the round: no flank, the round runs up to the top
            return c + s * ROUND_R, TOP
        a = math.acos(ROUND_R / dist)      # from the line of centres
        return c + s * ROUND_R * math.cos(a), TOP - ROUND_R * math.sin(a)
    t0, t1 = tangent(top_from, c_from, -1), tangent(top_to, c_to, 1)
    mid = lambda c, s: (c + s * ROUND_R * math.cos(math.radians(67.5)), TOP - ROUND_R * math.sin(math.radians(67.5)))
    top_from, top_to = min(top_from, t0[0]), max(top_to, t1[0])
    mid = lambda c, s: (c + s * ROUND_R * math.cos(math.radians(67.5)), TOP - ROUND_R * math.sin(math.radians(67.5)))

    def draw(wp):
        wp = wp.moveTo(top_from, TOP)
        if t0[0] != top_from:
            wp = wp.lineTo(*t0)
        wp = wp.threePointArc(mid(c_from, -1), (c_from, TOP - THICK)).lineTo(c_to, TOP - THICK).threePointArc(mid(c_to, 1), t1)
        return (wp.lineTo(top_to, TOP) if t1[0] != top_to else wp).close()
    return draw


(fx0, fx1), (fy0, fy1) = FOOTPRINT_X, FOOTPRINT_Y
(cx0, cx1), (cy0, cy1) = TREAD_X, TREAD_Y
along_x = side_profile(fx0, fx1, cx0, cx1)(cq.Workplane("XZ", origin=(0, fy1 + 1, 0))).extrude(fy1 - fy0 + 2)
along_y = side_profile(fy0, fy1, cy0, cy1)(cq.Workplane("YZ", origin=(fx0 - 1, 0, 0))).extrude(fx1 - fx0 + 2)
pad = along_x.intersect(along_y)

# -- interfaces, cut last -------------------------------------------------------------------------
below = cq.Workplane("XY", origin=(0, 0, TOP - THICK - 1)).pushPoints([(x, S.FOOT_SCREW_Y) for x in S.FOOT_SCREW_X])
pad = pad.cut(below.circle(SCREW_D / 2).extrude(THICK + 2)).cut(below.circle(SCREW_HEAD_D / 2).extrude(THICK + 1 - SCREW_HEAD_SEAT))

result = pad
