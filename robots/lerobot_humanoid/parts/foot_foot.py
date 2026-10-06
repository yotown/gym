"""LeRobot humanoid foot, written from its STEP: interfaces exact, the body simple.

Frame: the vendor's (mm): x forward (heel at -x), y across, z up from the sole. Symmetric about y 0.
An oval sole, a narrower deck on it, four ears at the back on the ankle-pitch axle (along y), and two
towers at the front on the ankle-roll axis (along x), its bearing through both, the roll servo's horn
screwed to the front one.
"""

import math

import cadquery as cq

# -- interfaces -- fixed ----------------------------------------------------------------------------
PITCH_AXIS = (-27.5, 35.0)                 # the ankle-pitch axle (x, z), along y
AXLE_D = 5.0                               # through all four ears
ROLL_AXIS_Z = 35.0                         # the ankle-roll axis, along x at y 0
ROLL_BEARING_D = 16.0                      # its bearing's seat, through both towers (a 5 x 16 x 5)
HORN_SCREWS = (20.0, 2.3, (90.0, 210.0, 330.0))   # the roll horn's three screws, through the front tower: circle, d, angles
EARS_Y = ((9.0, 14.0), (28.0, 32.0))       # the inner and the outer pair, each side  # measured
TOWERS_X = ((0.0, 7.5), (37.5, 45.0))      # the back and the front tower  # measured

# -- body: free -------------------------------------------------------------------------------------
SOLE_T = 10.0
SOLE = [(-89.1, 0.0), (-87.5, 7.0), (-83.0, 12.0), (-75.0, 16.0), (-60.0, 21.0), (-30.0, 27.6), (-15.0, 29.2), (30.0, 29.2), (47.3, 22.9), (57.5, 12.0), (60.3, 0.0)]   # half outline, heel to toe  # measured
DECK_TOP = 20.0
NARROW = 13.84                             # the deck's half width between the towers  # measured
DECK = [(-78.0, 0.0), (-76.9, 6.5), (-38.9, 24.7), (-38.06, 31.42), (-15.1, 31.42), (0.66, NARROW), (43.66, NARROW), (43.66, 19.89), (48.98, 21.5), (57.07, 6.21)]   # half outline  # measured
DECK_RIDGE_R = 8.0                         # between the towers the deck's top edges are rounded off: the roll joint swings over them  # measured
HEEL = [(-91.0, 8.0), (-75.0, 15.8), (-40.0, 19.5)]   # the heel's top falls away along this arc  # measured
EAR_BASE = (-38.056, -16.944)              # each ear's foot on the deck (x); its top round about the axle  # measured
EAR_R = 7.5
TOWER_HALF_WIDTH = 12.5                    # their round tops about the roll axis, as wide


def half_to_full(half):
    """A half outline (y >= 0, heel to toe) and its mirror, as one closed outline."""
    return half + [(x, -y) for x, y in reversed(half) if y > 0]


sole = cq.Workplane("XY").spline(half_to_full(SOLE), periodic=True).wire().extrude(SOLE_T)
deck = cq.Workplane("XY", origin=(0, 0, SOLE_T)).polyline(half_to_full(DECK)).close().extrude(DECK_TOP - SOLE_T)
narrow = [x for x, y in DECK if y == NARROW]   # that stretch, x from-to
deck = deck.edges(cq.selectors.BoxSelector((narrow[0] + 0.1, -40, DECK_TOP - 0.1), (narrow[1] - 0.1, 40, DECK_TOP + 0.1))).fillet(DECK_RIDGE_R)
foot = sole.union(deck)
heel = (cq.Workplane("XZ", origin=(0, 40, 0)).moveTo(HEEL[0][0], HEEL[0][1]).threePointArc(HEEL[1], HEEL[2])
        .lineTo(HEEL[2][0], 60).lineTo(-100, 60).lineTo(-100, HEEL[0][1]).close().extrude(80))
foot = foot.cut(heel)

# the ears: a foot on the deck, tangent sides up to a round about the axle
ax, az = PITCH_AXIS
for y0, y1 in EARS_Y:
    for s in (1, -1):
        ear = cq.Sketch().arc((ax, az), EAR_R, 0, 360).segment((EAR_BASE[0], DECK_TOP), (EAR_BASE[1], DECK_TOP)).hull()
        lo, hi = sorted((s * y0, s * y1))
        foot = foot.union(cq.Workplane("XZ", origin=(0, hi, 0)).placeSketch(ear).extrude(hi - lo))

# the towers: as wide as their round tops, standing on the deck
r = TOWER_HALF_WIDTH
for x0, x1 in TOWERS_X:
    tower = (cq.Workplane("YZ", origin=(x0, 0, 0)).center(0, (SOLE_T + ROLL_AXIS_Z) / 2).rect(2 * r, ROLL_AXIS_Z - SOLE_T).extrude(x1 - x0)
             .union(cq.Workplane("YZ", origin=(x0, 0, 0)).center(0, ROLL_AXIS_Z).circle(r).extrude(x1 - x0)))
    foot = foot.union(tower)

# -- interfaces, cut last -------------------------------------------------------------------------
foot = foot.cut(cq.Workplane("XZ", origin=(0, 40, 0)).center(ax, az).circle(AXLE_D / 2).extrude(80))
foot = foot.cut(cq.Workplane("YZ", origin=(TOWERS_X[0][0] - 1, 0, 0)).center(0, ROLL_AXIS_Z).circle(ROLL_BEARING_D / 2)
                .extrude(TOWERS_X[1][1] - TOWERS_X[0][0] + 2))
c, d, angles = HORN_SCREWS
pts = [(c / 2 * math.cos(math.radians(a)), ROLL_AXIS_Z + c / 2 * math.sin(math.radians(a))) for a in angles]
foot = foot.cut(cq.Workplane("YZ", origin=(TOWERS_X[1][0] - 1, 0, 0)).pushPoints(pts).circle(d / 2)
                .extrude(TOWERS_X[1][1] - TOWERS_X[1][0] + 2))

result = foot
