"""LeRobot humanoid femur (femur 12), written from its STEP: the thigh between the hip and the knee,
carrying the knee actuator. Its interfaces are exact; its body is one outline, cut layer by layer.

Frame: the STEP's (mm), seen from -y: the plane's x is the STEP's x, its y the STEP's z; depth is y,
from the back face (y 30) to the front (y 90). Three axes along y: the knee's at z 0, the knee
actuator's at z 224, the hip's at z 340.

The thigh is one outline (OUTLINE), extruded through the depth: a blade whose inner edge runs through the
actuator's axis, whose outer edge leaves the knee's boss tangent and bends, and whose top is the hip
clamp's split line, through the hip's axis. Below that line the hip actuator sits in half-bores. Layer by
layer the outline is cut: the hip's and the actuator's bores (each depth its own radius), a channel open
on -x in the middle layer (the knee rod runs in it), a slit that lets the front clamp the actuator, and
the knee's face, only below KNEE_FACE_TOP. Under the knee both faces of its boss taper in (KNEE_RELIEF).
Not drawn (body, free): the thin transition layers at y 45-47.5 and 71.5-72, the rounds inside the channel."""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
KNEE, ACT, HIP = (0.0, 0.0), (0.0, 224.0), (0.0, 340.0)
KNEE_BORE = ((16.0, 30.0, 72.5), (12.0, 72.5, 74.5), (16.0, 74.5, 87.0), (24.0, 87.0, 90.0))   # d, from, to
KNEE_SCREW_D, KNEE_SCREW_CIRCLE_D, KNEE_SCREW_FIRST_DEG = 2.5, 19.0, 60.0   # the knee's three screws
HIP_BOLT_FIRST_DEG, ACT_BOLT_FIRST_DEG = 230.55, 298.28    # 45 deg apart  # measured
ACT_ACCESS_D = 8.0                         # through the back wall, to reach those bolts
# the hip actuator's half-bores below the split line, and the knee actuator's: radius, y from-to
HIP_BORES = ((35.0, 30.0, 32.0), (54.0, 32.0, 72.0), (42.5, 72.0, 88.0))
ACT_BORES = ((60.0, 45.0, 72.0), (35.0, 72.0, 74.5), (54.0, 74.5, 88.0))   # clearance, ledge, seat
FRONT = (72.0, 88.0)                       # the front layer, y from-to: against femur_22
KNEE_FACE_TOP = 138.8                      # the knee's face, up to here  # measured

# -- body: free -------------------------------------------------------------------------------------
KNEE_SCREWS_Y = (73.25, 87.0)              # the knee screws' holes, y from-to: they run between the bores, so free
ACT_ACCESS_Y = (30.0, 45.0)                # the access bores, y from-to
BACK = (30.0, 45.0)                        # the layers, y from-to
CHANNEL = (45.0, 72.0)
FACE = (88.0, 90.0)
HIP_BOLTS_Y = (30.0, 88.0)                 # the holes of the bolts and pins: y from-to
ACT_BOLTS_Y = (72.0, 74.5)
PINS_Y = (65.0, 88.0)
SPLIT_DEG = 28.05                          # the hip clamp's split line, through the hip's axis  # measured
INNER_EDGE_DEG = 95.78                     # the blade's inner edge, through the actuator's axis  # measured
SLIT = (-7.94, 2.06)                       # the front's clamp slit, between the hip's bore and the actuator's: x from-to  # measured
# rounds of the outline: their centres (the knee's boss and nose are about the knee's axis)
BEND_AT, CURL_AT = (16.46, 59.96), (-13.76, 61.94)        # R30 each  # measured
KNEE_TOE_AT, KNEE_HEEL_AT, KNEE_FOOT_AT = (-5.16, 27.01), (-22.61, -15.66), (2.38, -14.77)   # R15, R15, R10  # measured
ROD_TURN_AT, ROD_TURN_R = (0.0, 50.0), 15.0              # in the channel, room for the knee rod's turn
HIP_ACT_ROUND_AT, HIP_ACT_ROUND_R = (0.0, 274.0), 20.0   # in the channel, the hip's and the actuator's bores joined
WING_CLEAR_R = 70.0                        # in the channel, the wing above the actuator: clear of it by this, about its axis


def on(centre, r, deg):
    return (centre[0] + r * math.cos(math.radians(deg)), centre[1] + r * math.sin(math.radians(deg)))


# -- interfaces -- fixed: the outline, its knee boss about the knee's axis --------------------------
# the outline: the knee's boss (R25 about its axis), the outer edge, the hip's boss (R55), the split line out
# to the wing, the inner edge down to the knee, and the knee's toe, nose (R12.5), heel and foot
OUTLINE = [(3.97, -24.64), ("arc", (23.45, -8.54), KNEE, True), ("line", (44.65, 49.70)),
           ("arc", (46.29, 56.77), BEND_AT, True), ("line", (64.75, 229.70)), ("line", (54.22, 349.24)),
           ("arc", on(HIP, 55.0, SPLIT_DEG), HIP, True), ("line", on(HIP, -60.65, SPLIT_DEG)),
           ("line", (-4.31, 266.59)), ("line", (16.09, 64.95)), ("arc", (15.72, 56.37), CURL_AT, False),
           ("line", (8.72, 21.33)), ("arc", (-2.35, 12.28), KNEE_TOE_AT, False), ("arc", (-10.28, -7.12), KNEE, True),
           ("arc", (-7.62, -15.12), KNEE_HEEL_AT, False), ("arc", (3.97, -24.64), KNEE_FOOT_AT, True)]
# where the channel and the front's ledge are open about the knee: left of this, from the boss up
KNEE_OPEN = [(16.79, -18.47), ("line", (10.15, -7.30)), ("arc", (7.04, 10.33), KNEE, True)]

# -- body: free -------------------------------------------------------------------------------------
LEDGE_OPEN = KNEE_OPEN + [("line", (15.72, 56.37)), ("arc", (16.09, 64.95), CURL_AT, True),
                          ("line", (-80.0, 64.95)), ("line", (-80.0, -40.0)), ("line", (29.6, -40.0))]
CHANNEL_OPEN = KNEE_OPEN + [("line", (13.16, 42.81)), ("line", (15.07, 52.91)), ("line", (15.72, 56.37)),
                            ("arc", (16.09, 64.95), CURL_AT, True), ("line", (15.47, 71.05)), ("line", (17.61, 166.64)),
                            ("line", (-80.0, 166.64)), ("line", (-80.0, -40.0)), ("line", (29.6, -40.0))]
# the knee relief: under the knee, each face of the boss tapers in, a cone about the knee's axis: from the heel
# round to the side wall (deg), radius at the face and at its foot, y at the face and at the foot
KNEE_RELIEF = ((180.0, 312.3), (22.1, 10.0), ((37.5, 46.0), (82.5, 74.0)))   # measured


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
            wp = wp.threePointArc((cx + r * math.cos(a0 + sweep / 2), cy + r * math.sin(a0 + sweep / 2)), end)
        here = seg[1]
    return wp.close()


def at_y(y):
    """A plane at that y, seen from -y (x is x, y is the STEP's z); extrude(-d) goes d deeper in y."""
    return cq.Workplane(cq.Plane(origin=(0, y, 0), xDir=(1, 0, 0), normal=(0, -1, 0)))


def between(y0, y1):
    """(a plane at y0, the extrude that reaches y1)."""
    return at_y(y0), y0 - y1


def disc(at, r, y0, y1):
    wp, d = between(y0, y1)
    return wp.center(*at).circle(r).extrude(d)


# the blade, and the knee's face below KNEE_FACE_TOP
wp, d = between(BACK[0], FRONT[1])
femur = profile(wp, OUTLINE).extrude(d)
wp, d = between(*FACE)
femur = femur.union(profile(wp, OUTLINE).extrude(d).intersect(wp.center(0, KNEE_FACE_TOP / 2 - 50).rect(200, KNEE_FACE_TOP + 100).extrude(d)))

# the hip's and the actuator's bores
for at, bores in ((HIP, HIP_BORES), (ACT, ACT_BORES)):
    for r, y0, y1 in bores:
        femur = femur.cut(disc(at, r, y0, y1))

# the channel: open on -x about the knee and up to the actuator, the rod's turn, the two bores joined,
# and clear of the actuator under the wing (a half disc on the inner side of the inner edge)
wp, d = between(*CHANNEL)
femur = femur.cut(profile(wp, CHANNEL_OPEN).extrude(d))
femur = femur.cut(disc(ROD_TURN_AT, ROD_TURN_R, *CHANNEL)).cut(disc(HIP_ACT_ROUND_AT, HIP_ACT_ROUND_R, *CHANNEL))
wp, d = between(*CHANNEL)
femur = femur.cut(wp.moveTo(*on(ACT, WING_CLEAR_R, INNER_EDGE_DEG)).threePointArc(on(ACT, WING_CLEAR_R, INNER_EDGE_DEG + 90),
                                                                                   on(ACT, WING_CLEAR_R, INNER_EDGE_DEG + 180)).close().extrude(d))
# the front's ledge (the actuator's R35), open about the knee; the front's clamp slit
ledge = ACT_BORES[1][1:]
wp, d = between(*ledge)
femur = femur.cut(profile(wp, LEDGE_OPEN).extrude(d))
wp, d = between(ledge[1], FRONT[1])
femur = femur.cut(wp.center((SLIT[0] + SLIT[1]) / 2, (ACT[1] + HIP[1]) / 2).rect(SLIT[1] - SLIT[0], HIP[1] - ACT[1]).extrude(d))

# the knee's relief: the sector under the knee, less the cone
(a0, a1), (r_face, r_foot), faces = KNEE_RELIEF
for y_face, y_foot in faces:
    depth = abs(y_foot - y_face)
    sector = (at_y(y_face).moveTo(*KNEE).lineTo(*on(KNEE, 40, a0)).threePointArc(on(KNEE, 40, (a0 + a1) / 2), on(KNEE, 40, a1))
              .close().extrude(-depth if y_foot > y_face else depth))
    cone = cq.Solid.makeCone(r_face, r_foot, depth, cq.Vector(KNEE[0], y_face, KNEE[1]), cq.Vector(0, 1 if y_foot > y_face else -1, 0))
    femur = femur.cut(sector.cut(cq.Workplane().add(cone)))

# the knee's bearing and its screws
for d, y0, y1 in KNEE_BORE:
    femur = femur.cut(disc(KNEE, d / 2, y0, y1))
wp, d = between(*KNEE_SCREWS_Y)
femur = femur.cut(wp.center(*KNEE).polarArray(KNEE_SCREW_CIRCLE_D / 2, KNEE_SCREW_FIRST_DEG, 360, 3).circle(KNEE_SCREW_D / 2).extrude(d))

# the hip's and the actuator's bolts (and the access bores to the actuator's), the pins
for at, first, ys, bolt_d in [(HIP, HIP_BOLT_FIRST_DEG, HIP_BOLTS_Y, S.FEMUR_BOLT_D), (ACT, ACT_BOLT_FIRST_DEG, ACT_BOLTS_Y, S.FEMUR_BOLT_D),
                              (ACT, ACT_BOLT_FIRST_DEG, ACT_ACCESS_Y, ACT_ACCESS_D)]:
    wp, d = between(*ys)
    femur = femur.cut(wp.center(*at).polarArray(S.FEMUR_BOLT_CIRCLE_D / 2, first, 135, 4).circle(bolt_d / 2).extrude(d))
wp, d = between(*PINS_Y)
for pin_d, pts in S.FEMUR_PINS.items():
    femur = femur.cut(wp.pushPoints(pts).circle(pin_d / 2).extrude(d))
result = femur
