"""LeRobot humanoid femur cover (femur 22), written from its STEP: a 2 mm plate around the knee
actuator, a rib and a flange on the actuator's side, and a pedestal with a stub axle at the
upper end for the knee rod's bearing.

Frame: the STEP's (mm), seen from -y: the plane's x is the STEP's x, its y the STEP's z, and
depth runs towards -y from the plate's face at y -28. Two axes along y: the knee actuator's at
(0, 224) and the eye's at (0, 340). The outlines are the designer's polygons: their corners are
measured, the arcs are about those two axes where they say so. Not drawn: the R2 and R3 blends
at the pedestal's root."""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)
SMALL_BEARING = S.SMALL_BEARING

# -- interfaces -- fixed ----------------------------------------------------------------------------
KNEE_AT, EYE_AT = (0.0, 224.0), (0.0, 340.0)
EYE_BOLT_FIRST_DEG, KNEE_BOLT_FIRST_DEG = 230.55, 298.28  # measured
AXLE_TO = 37.0                             # the 15x21x4 bearing's axle, to that depth
CAP_SCREW_D, CAP_SCREW_CIRCLE_D = 2.5, 8.0            # three, into the axle's end
CAP_SCREW_DEPTH = 5.0                                 # not in the model: the cap's screws
PEDESTAL_TO = 33.0                                    # the pedestal's face, the bearing's stop
PLATE_FROM = 28.0
RIB_TO = 54.0
PLATE = [(55.045, 138.815), ("line", (8.618, 138.815)), ("line", (5.435, 170.274)),
         ("arc", (-14.613, 275.985), KNEE_AT, True), ("line", (-53.524, 311.478)), ("line", (-11.540, 333.850)),
         ("arc", (-8.930, 338.883), (-13.892, 338.263), True), ("arc", (5.907, 346.790), EYE_AT, False),
         ("arc", (11.540, 346.150), (9.189, 350.562), True), ("line", (48.538, 365.866)),
         ("arc", (54.218, 349.241), EYE_AT, False), ("line", (64.749, 229.704))]

# -- body: free -------------------------------------------------------------------------------------
PEDESTAL_D = 18.0                          # on the bearing's inner race only: keep 15 < d < 19
PLATE_TO = 30.0
FLANGE_TO = 59.0
RIB_OUTER_AT = (-4.337, 220.642)                      # the rib's outer arc's centre  # measured
RIB = [(5.939, 165.300), ("line", (5.435, 170.274)), ("arc", (-14.613, 275.985), KNEE_AT, True),
       ("line", (11.595, 286.476)), ("arc", (45.992, 175.312), RIB_OUTER_AT, False)]

# -- interfaces -- fixed: the flange's outline ------------------------------------------------------
FLANGE = [(2.452, 184.075), ("line", (5.022, 170.234)), ("arc", (5.435, 170.274), KNEE_AT, True),
          ("line", (5.939, 165.300)), ("line", (45.992, 175.312)), ("arc", (11.595, 286.476), RIB_OUTER_AT, True),
          ("line", (-14.613, 275.985)), ("line", (-12.043, 262.144)), ("arc", (2.452, 184.075), KNEE_AT, False)]

# -- body: free -------------------------------------------------------------------------------------

# outlines: ("line", corner) or ("arc", corner, centre, ccw); every corner measured


def profile(wp, outline):
    """An outline from its first corner, then lines and arcs about their centres."""
    wp = wp.moveTo(*outline[0])
    here = outline[0]
    for seg in outline[1:]:
        if seg[0] == "line":
            wp = wp.lineTo(*seg[1])
        else:
            _, end, (cx, cy), ccw = seg
            a0 = math.atan2(here[1] - cy, here[0] - cx)
            a1 = math.atan2(end[1] - cy, end[0] - cx)
            sweep = (a1 - a0) % (2 * math.pi) if ccw else -((a0 - a1) % (2 * math.pi))
            r = math.hypot(here[0] - cx, here[1] - cy)
            mid = (cx + r * math.cos(a0 + sweep / 2), cy + r * math.sin(a0 + sweep / 2))
            wp = wp.threePointArc(mid, end)
        here = seg[1]
    return wp.close()


def at_depth(d):
    """A plane at y = -d, extruding towards -y: x is the STEP's x, y the STEP's z."""
    return cq.Workplane(cq.Plane(origin=(0, -d, 0), xDir=(1, 0, 0), normal=(0, -1, 0)))


cover = profile(at_depth(PLATE_FROM), PLATE).extrude(PLATE_TO - PLATE_FROM)
cover = cover.union(profile(at_depth(PLATE_TO), RIB).extrude(RIB_TO - PLATE_TO))
cover = cover.union(profile(at_depth(RIB_TO), FLANGE).extrude(FLANGE_TO - RIB_TO))
cover = cover.union(at_depth(PLATE_FROM).center(*EYE_AT).circle(PEDESTAL_D / 2).extrude(PEDESTAL_TO - PLATE_FROM))
cover = cover.union(at_depth(PEDESTAL_TO).center(*EYE_AT).circle(SMALL_BEARING.bore / 2).extrude(AXLE_TO - PEDESTAL_TO))

cover = cover.cut(at_depth(AXLE_TO - CAP_SCREW_DEPTH).center(*EYE_AT).polarArray(CAP_SCREW_CIRCLE_D / 2, 0, 360, 3)
                  .circle(CAP_SCREW_D / 2).extrude(CAP_SCREW_DEPTH))
cover = cover.cut(at_depth(PLATE_FROM).center(*EYE_AT).polarArray(S.FEMUR_BOLT_CIRCLE_D / 2, EYE_BOLT_FIRST_DEG, 135, 4)
                  .circle(S.FEMUR_BOLT_D / 2).extrude(PLATE_TO - PLATE_FROM))
cover = cover.cut(at_depth(RIB_TO).center(*KNEE_AT).polarArray(S.FEMUR_BOLT_CIRCLE_D / 2, KNEE_BOLT_FIRST_DEG, 135, 4)
                  .circle(S.FEMUR_BOLT_D / 2).extrude(FLANGE_TO - RIB_TO))
for d, pts in S.FEMUR_PINS.items():
    cover = cover.cut(at_depth(PLATE_FROM).pushPoints(pts).circle(d / 2).extrude(PLATE_TO - PLATE_FROM))
result = cover
