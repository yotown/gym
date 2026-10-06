"""Open Duck Mini v2 sole insert (PLA), written from its STEP: interfaces exact, the body simple.

A slab in the foot's sole pocket (foot_top / foot_side), its ends chamfered as the pocket's, and a tongue
below it through the pocket's lip, flush with the foot's sole; the sole pad (foot_bottom_tpu) screws
into it from below. Every face of it fits something: it is all interface.

Frame: the vendor's (mm): the foot's, z up; the slab lies in (x, y).
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)
INSERT = S.INSERT

# -- interfaces -- fixed ----------------------------------------------------------------------------
SLAB_X = (-53.25, 39.725)                  # in the foot's pocket: x,
SLAB_Y = (76.15, 103.85)                   # y,
SLAB_Z = (-249.625, -245.625)              # z
SLAB_CHAMFER = 4.82                        # its ends (x) at the top, as the pocket's  # measured
TONGUE_X = (-44.75, 31.225)                # through the pocket's lip: x,
TONGUE_Y = (79.65, 100.35)                 # y,
PILOT_D = 3.2                              # and its pilot past it

# -- body: free -------------------------------------------------------------------------------------
PILOT_PAST = 0.2

x0, x1 = SLAB_X
y0, y1 = SLAB_Y
z0, z1 = SLAB_Z
c = SLAB_CHAMFER
end = [(x0, z0), (x1, z0), (x1, z1 - c * 0.8), (x1 - c, z1), (x0 + c, z1), (x0, z1 - c * 0.8)]
insert = cq.Workplane("XZ", origin=(0, y1, 0)).polyline(end).close().extrude(y1 - y0)
tx0, tx1 = TONGUE_X
ty0, ty1 = TONGUE_Y
insert = insert.union(cq.Workplane("XY", origin=(0, 0, S.FOOT_SOLE_Z)).center((tx0 + tx1) / 2, (ty0 + ty1) / 2).rect(tx1 - tx0, ty1 - ty0).extrude(z0 - S.FOOT_SOLE_Z))

# -- interfaces, cut last -------------------------------------------------------------------------
below = cq.Workplane("XY", origin=(0, 0, S.FOOT_SOLE_Z)).pushPoints([(x, S.FOOT_SCREW_Y) for x in S.FOOT_SCREW_X])
insert = insert.cut(below.circle(INSERT.hole_d / 2).extrude(INSERT.depth)).cut(below.circle(PILOT_D / 2).extrude(INSERT.depth + PILOT_PAST))

result = insert
