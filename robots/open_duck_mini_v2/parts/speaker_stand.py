"""Open Duck Mini v2 speaker stand, written from its STEP: interfaces exact, the body simple.

A bent bracket: a top leg screwed up under the head's top (four screws; two small bosses below it), bent
down into a leg tilted back that carries the speaker -- nested in a square pocket in its outer face, its opening, and four screws on a square into
bosses inside, blind -- with a gusset in the bend at the middle. The legs' free corners rounded.

Frame: the stand's own (x', y', z) in mm, turned S.SPEAKER_TURN about z from the vendor's: x' across the stand,
y' from the tilted leg towards the top leg's free end, z up (the vendor's z).
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)


# -- interfaces -- fixed ----------------------------------------------------------------------------
# this part is not in the model: what it fits is declared
SPEAKER_AT = (56.273, -51.176, 135.701)    # the speaker's axis on the tilted leg's outer face (x', y', z); not in the model: the speaker
SPEAKER_D = 18.9                           # its opening; not in the model: the speaker
SPEAKER_POCKET_SIDE = 38.0                 # it nests in the leg's outer face, a square; not in the model: the speaker  # measured
SPEAKER_POCKET_DEEP = 1.4                  # not in the model: the speaker  # measured
SPEAKER_POCKET_R = 2.0                     # its corners; not in the model: the speaker  # measured
SPEAKER_SCREW_SQUARE = 32.0                # its screws, on a square in the leg,
SPEAKER_SCREW_D = 2.05
SPEAKER_SCREW_TO = 6.0                     # into bosses inside, ending this far in from the leg's outer face; not in the model: the speaker's screws
TOP_FACE_Z = 161.11                        # the top leg's upper face, under the head's top; not in the model: this part
TOP_SCREW_X = (40.276, 72.277)             # through the top leg into the head: x',
TOP_SCREW_Y = (-23.235, -31.235)           # y'
TOP_SCREW_D = 2.7
TOP_PIN_X = (49.901, 62.651)               # pins under the top leg: x',
TOP_PIN_Y = -34.236                        # y'
TOP_PIN_D = 2.05
TOP_PIN_TO = 5.0                           # in bosses ending this far below the top face; not in the model: the pins

# -- body: free -------------------------------------------------------------------------------------
X = (34.27, 78.28)                         # x' from-to
T = 3.0                                    # the bracket's thickness
TOP_FREE_Y = -19.74                        # the top leg's free end (y')
LEG_END = 97.775                           # its free end: its level along the leg  # measured
BEND_R = 5.0                               # the bend, outside
CORNER_R = 3.0                             # the free corners
GUSSET = (3.0, 50.0, -128.832)             # in the bend at the middle: thick (x'), its edge's slope (deg), its level  # measured
SPEAKER_BOSS_D = 6.0                       # the speaker screws' bosses inside the leg
TOP_PIN_BOSS_D = 4.0                       # the pins' bosses under the top leg

c, s = math.cos(math.radians(S.SPEAKER_TILT_DEG)), math.sin(math.radians(S.SPEAKER_TILT_DEG))
n = (c, -s)                                # the tilted leg's normal in (y', z), outwards = -n
along = (s, c)                             # up the leg
LEG_OUT = n[0] * SPEAKER_AT[1] + n[1] * SPEAKER_AT[2]   # the tilted leg's outer face, through the speaker's axis point


def meet(l1, n1, l2, n2):
    """The point (y', z) on both lines n . p = l."""
    det = n1[0] * n2[1] - n1[1] * n2[0]
    return ((l1 * n2[1] - l2 * n1[1]) / det, (n1[0] * l2 - n2[0] * l1) / det)


top, free = TOP_FACE_Z, TOP_FREE_Y
outer_top = meet(LEG_OUT, n, top, (0, 1))
inner_top = meet(LEG_OUT + T, n, top - T, (0, 1))
outer_end = meet(LEG_OUT, n, LEG_END, along)
inner_end = meet(LEG_OUT + T, n, LEG_END, along)
profile = [(free, top), outer_top, outer_end, inner_end, inner_top, (free, top - T)]
x0, x1 = X
stand = cq.Workplane("YZ", origin=(x0, 0, 0)).polyline(profile).close().extrude(x1 - x0)
stand = stand.edges("|X").edges(cq.selectors.NearestToPointSelector((x0, outer_top[0], outer_top[1]))).fillet(BEND_R)
gt, slope, level = GUSSET
g = (math.sin(math.radians(slope)), -math.cos(math.radians(slope)))
gusset = [inner_top, meet(level, g, top - T, (0, 1)), meet(level, g, LEG_OUT + T, n)]
xm = (x0 + x1) / 2
stand = stand.union(cq.Workplane("YZ", origin=(xm - gt / 2, 0, 0)).polyline(gusset).close().extrude(gt))

# -- interfaces, cut last -------------------------------------------------------------------------
(sx, sy, sz), sd = SPEAKER_AT, SPEAKER_D
axis = cq.Vector(0, n[0], n[1])            # into the leg from outside
leg = cq.Plane(origin=(sx, sy, sz), xDir=(1, 0, 0), normal=axis)
stand = stand.cut(cq.Workplane(leg).workplane(offset=-1).circle(sd / 2).extrude(T + 2))
ps, pdeep, pr = SPEAKER_POCKET_SIDE, SPEAKER_POCKET_DEEP, SPEAKER_POCKET_R
stand = stand.cut(cq.Workplane(leg).workplane(offset=-1).placeSketch(cq.Sketch().rect(ps, ps).vertices().fillet(pr)).extrude(1 + pdeep))
side, d, boss, to = SPEAKER_SCREW_SQUARE, SPEAKER_SCREW_D, SPEAKER_BOSS_D, SPEAKER_SCREW_TO
square = [(u * side / 2, v * side / 2) for u in (1, -1) for v in (1, -1)]
stand = stand.union(cq.Workplane(leg).workplane(offset=T).pushPoints(square).circle(boss / 2).extrude(to - T))
stand = stand.cut(cq.Workplane(leg).workplane(offset=pdeep).pushPoints(square).circle(d / 2).extrude(to - pdeep))
xs, ys, d = TOP_SCREW_X, TOP_SCREW_Y, TOP_SCREW_D
stand = stand.cut(cq.Workplane("XY", origin=(0, 0, top - T - 1)).pushPoints([(x, y) for x in xs for y in ys]).circle(d / 2).extrude(T + 2))
xs, y, d, boss, to = TOP_PIN_X, TOP_PIN_Y, TOP_PIN_D, TOP_PIN_BOSS_D, TOP_PIN_TO
pins = [(x, y) for x in xs]
stand = stand.union(cq.Workplane("XY", origin=(0, 0, top - to)).pushPoints(pins).circle(boss / 2).extrude(to - T))
stand = stand.cut(cq.Workplane("XY", origin=(0, 0, top - to - 1)).pushPoints(pins).circle(d / 2).extrude(to + 2))

result = stand.rotate((0, 0, 0), (0, 0, 1), S.SPEAKER_TURN)
