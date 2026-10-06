"""Open Duck Mini v2 foot (the top half), written from its STEP: interfaces exact, the body simple.

The foot's outline (in x, z) is the hull of three rounds -- at the ankle, the heel and the toe -- cut flat
at the sole. Below the tray's top it runs the foot's whole width (y); above, only the plate on the
ankle servo's horn (the horn's bore and four screws counterbored from outside, a slot to the top). In
the tray's underside a pocket takes the sole insert (foot_bottom_pla) through a lip; two windows go up
through the tray; two pins tie it to foot_side. The plate's outer foot edge rounded. foot_side is this design
facing the other way (FOOT).

Frame: the vendor's (mm). The ankle axis runs along y through ANKLE (x, z); the foot's back face (onto
foot_side) is y = BACK.
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)
HORN, HORN_SCREW = S.HORN, S.HORN_SCREW

H = globals().get("FOOT", {})              # foot_side's differences (it runs this program, then is mirrored across the foot)

# -- interfaces -- fixed ----------------------------------------------------------------------------
ANKLE_X, ANKLE_Z = -16.06, -222.3          # the ankle servo's axis, along y
HORN_SEAT_Y = 109.05                       # the plate's inner face: the horn sits on it
HORN_THROUGH_D = 7.0                       # then through
HORN_SCREW_HEAD_SEAT = 3.0                 # out from the horn's seat
BACK_Y = H.get("back", 79.15)              # the tray's back face, onto foot_side
PIN_X = [-43.25, 29.725]                   # the two pins between foot_top and foot_side,
PIN_Z = -241.625
PIN_HOLES = H.get("pin_holes", [(4.0, 79.15, 84.95), (2.0, 79.15, 100.15)])   # along y: d, from, to
SOLE_POCKET_X = (-53.25, 39.725)           # the sole insert's pocket: x,
SOLE_POCKET_Z = (-251.625, -245.125)       # z
SOLE_POCKET_CHAMFER = 4.82                 # its ends chamfered (x, at the top)  # measured
SOLE_LIP = H.get("sole_lip", ((-45.25, 31.725), 100.85))   # the lip the insert's tongue passes: x, to y; or none

# -- body: free -------------------------------------------------------------------------------------
HORN_BORE_D = 7.6                          # clears the horn's hub, into the seat (with the relief)
HORN_BORE_DEEP = 1.5
SOLE_POCKET_TO_Y = H.get("pocket_to", 104.35)   # the sole pocket runs to here (past the insert)
PLATE_T = 5.0                              # the plate on the horn
TRAY_TOP_Z = -237.41
ROUNDS = (((-14.792, -217.629), 10.0), ((-43.652, -249.084), 12.0), ((35.851, -253.528), 12.0))   # the outline's: ankle, heel, toe  # measured
WINDOWS = H.get("windows", ([(-34.962, -28.562), (15.037, 21.438)], (80.1, 99.9)))   # through the tray: x from-to each, y from-to; or none  # measured
FOOT_EDGE = H.get("foot_edge", ((102.05, -245.437), 12.0))   # the plate's outer foot edge: rounded about this (y, z), r  # measured
RELIEF = (7.6, 1.5, 1.0)                   # clears the horn: from its bore to the top, in the seat: wide, deep, corner r
PLATE_OUT_Y = HORN_SEAT_Y + PLATE_T


def plane_y(y, into):
    """The plane y = const, (x, z) its coordinates; extrude(d) goes d towards into (+1: +y, -1: -y)."""
    return cq.Workplane(cq.Plane(origin=(0, y, 0), xDir=(1, 0, 0), normal=(0, -1, 0))) if into < 0 else \
        cq.Workplane(cq.Plane(origin=(0, y, 0), xDir=(-1, 0, 0), normal=(0, 1, 0)))


def x_(x, into):                           # the +y planes see x mirrored
    return x if into < 0 else -x


outline = cq.Sketch()
for c, r in ROUNDS:
    outline = outline.arc(c, r, 0, 360)
outline = outline.hull()
foot = plane_y(PLATE_OUT_Y, -1).placeSketch(outline).extrude(PLATE_OUT_Y - BACK_Y)
foot = foot.cut(cq.Workplane("XY", origin=(0, 0, S.FOOT_SOLE_Z - 30)).center(0, (BACK_Y + PLATE_OUT_Y) / 2).rect(300, 100).extrude(30))
foot = foot.cut(cq.Workplane("XY", origin=(0, 0, TRAY_TOP_Z)).center(0, (BACK_Y - 1 + HORN_SEAT_Y) / 2).rect(300, HORN_SEAT_Y - BACK_Y + 1).extrude(100))
(ey, ez), er = FOOT_EDGE
corner = cq.Workplane("YZ", origin=(-200, 0, 0)).center((ey + PLATE_OUT_Y + 1) / 2, (ez + S.FOOT_SOLE_Z - 1) / 2).rect(PLATE_OUT_Y + 1 - ey, ez - S.FOOT_SOLE_Z + 1).extrude(400)
foot = foot.cut(corner.cut(cq.Workplane("YZ", origin=(-200, 0, 0)).center(ey, ez).circle(er).extrude(400)))

# the sole insert's pocket and lip, the windows
(px0, px1), (pz0, pz1), py, ch = SOLE_POCKET_X, SOLE_POCKET_Z, SOLE_POCKET_TO_Y, SOLE_POCKET_CHAMFER
pocket = [(px0, pz0), (px1, pz0), (px1, pz1 - ch * 0.8), (px1 - ch, pz1), (px0 + ch, pz1), (px0, pz1 - ch * 0.8)]
foot = foot.cut(plane_y(py, -1).polyline(pocket).close().extrude(py - BACK_Y + 1))
if SOLE_LIP:
    (lx0, lx1), ly = SOLE_LIP
    foot = foot.cut(cq.Workplane("XY", origin=(0, 0, S.FOOT_SOLE_Z - 1)).center((lx0 + lx1) / 2, (BACK_Y - 1 + ly) / 2).rect(lx1 - lx0, ly - BACK_Y + 1).extrude(pz0 - S.FOOT_SOLE_Z + 1.01))
if WINDOWS:
    xs_w, (wy0, wy1) = WINDOWS
    for wx0, wx1 in xs_w:
        foot = foot.cut(cq.Workplane("XY", origin=(0, 0, pz1 - 0.01)).center((wx0 + wx1) / 2, (wy0 + wy1) / 2).rect(wx1 - wx0, wy1 - wy0).extrude(TRAY_TOP_Z - pz1 + 1))

w, deep, r = RELIEF
foot = foot.cut(plane_y(HORN_SEAT_Y, 1).center(x_(ANKLE_X, 1), ANKLE_Z + 10).rect(w, 20).extrude(deep).edges("|Y").fillet(r))

# -- interfaces, cut last -------------------------------------------------------------------------
for d, y0, y1 in PIN_HOLES:
    foot = foot.cut(plane_y(y1, -1).pushPoints([(x, PIN_Z) for x in PIN_X]).circle(d / 2).extrude(y1 - y0))
foot = foot.cut(plane_y(HORN_SEAT_Y, 1).center(x_(ANKLE_X, 1), ANKLE_Z).circle(HORN_BORE_D / 2).extrude(HORN_BORE_DEEP))
foot = foot.cut(plane_y(PLATE_OUT_Y, -1).center(ANKLE_X, ANKLE_Z).circle(HORN_THROUGH_D / 2).extrude(PLATE_T))
pts = HORN.points(at=(ANKLE_X, ANKLE_Z))
foot = foot.cut(plane_y(PLATE_OUT_Y, -1).pushPoints(pts).circle(HORN_SCREW.hole_d / 2).extrude(PLATE_T))
foot = foot.cut(plane_y(PLATE_OUT_Y + 1, -1).pushPoints(pts).circle(HORN_SCREW.head_d / 2).extrude(PLATE_OUT_Y + 1 - HORN_SEAT_Y - HORN_SCREW_HEAD_SEAT))

result = foot.mirror("XZ", basePointVector=(0, H["mirror_about_y"], 0)) if "mirror_about_y" in H else foot
