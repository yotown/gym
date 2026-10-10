"""Open Duck Mini v2 leg spacer, written from its STEP: interfaces exact, the body simple.

A bar along y between the knee-to-ankle sheets (as long as the horn servo's horn-to-idler span): a bow-tie section (two lobes, one round each rod, and a
waist between them: from above and below a V of WAIST_SLOPE_DEG, rounded R10 at its foot) holding the two rods,
each through a 2 mm hole with a 4 mm counterbore at both ends; two 6 mm holes go through the waist across it.

Frame: the vendor's (mm). The bar runs along y from Y_FROM to Y_TO; its section is in (x, z) about AXIS.
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
HORN_SERVO = S.SERVOS["sts3215"]           # the servo whose horn and idler the leg's two sheets sit on
AXIS_X, AXIS_Z = -16.06, -163.975          # the bar's middle
HORN_FACE_Y = 109.15                       # the outer sheet's seat (the horn's face); the inner's is the idler's face
SHEET_GAP = 0.1                            # clear of each sheet's seat
Y_FROM, Y_TO = HORN_FACE_Y - HORN_SERVO.faces.idler_face + SHEET_GAP, HORN_FACE_Y - SHEET_GAP   # between the leg's two sheets
ROD_D = 2.0                                # through,
ROD_BORE_D = 4.0                           # counterbored at both ends
ROD_BORE_DEEP = 5.8
CROSS_D = 6.0                              # the two holes across the waist (along z),
CROSS_Y = (80.0, 100.0)                    # at

# -- body: free -------------------------------------------------------------------------------------
WIDTH = 28.61                              # the section: wide at its foot (-z, before rounding),  # measured
HEIGHT = 10.0                              # tall,
CORNER_R = 2.0                             # its corners rounded
END_LEAN_DEG = 7.24                        # its ends lean in towards +z  # measured
WAIST_R = 10.0                             # the waist: two rounded Vs, above and below,
WAIST = 4.88                               # leaving this much between
WAIST_SLOPE_DEG = 16.7                     # the V's flanks, from the bar's faces  # measured


def along_y(y_from, y_to):
    """A plane at y_to seen from +y, its x along x and its y along z; extrude(d) goes d towards -y."""
    return cq.Workplane(cq.Plane(origin=(0, y_to, 0), xDir=(1, 0, 0), normal=(0, -1, 0))), y_to - y_from


wp, length = along_y(Y_FROM, Y_TO)
cx, cz = AXIS_X, AXIS_Z
top = WIDTH / 2 - HEIGHT * math.tan(math.radians(END_LEAN_DEG))
section = [(-WIDTH / 2, -HEIGHT / 2), (WIDTH / 2, -HEIGHT / 2), (top, HEIGHT / 2), (-top, HEIGHT / 2)]
spacer = wp.center(cx, cz).polyline(section).close().extrude(length).edges("|Y").fillet(CORNER_R)
# each V: the round at its foot, and its flanks tangent to it, out past the bar's face
t = math.radians(WAIST_SLOPE_DEG)
for side in (1, -1):                       # above, below
    c = side * (WAIST / 2 + WAIST_R)       # the round's centre
    left, right = (-WAIST_R * math.sin(t), c - side * WAIST_R * math.cos(t)), (WAIST_R * math.sin(t), c - side * WAIST_R * math.cos(t))
    out = WIDTH                            # far enough along the flanks to leave the bar
    v = (wp.center(cx, cz).moveTo(*left).threePointArc((0, c - side * WAIST_R), right)
         .lineTo(right[0] + out, right[1] + side * out * math.tan(t)).lineTo(right[0] + out, side * HEIGHT)
         .lineTo(left[0] - out, side * HEIGHT).lineTo(left[0] - out, left[1] + side * out * math.tan(t)).close())
    spacer = spacer.cut(v.extrude(length))

# -- interfaces, cut last -------------------------------------------------------------------------
rods = [(-S.LEG_ROD_PITCH / 2, 0), (S.LEG_ROD_PITCH / 2, 0)]
spacer = spacer.cut(wp.center(cx, cz).pushPoints(rods).circle(ROD_D / 2).extrude(length))
for y in (Y_TO, Y_FROM + ROD_BORE_DEEP):
    bore, d = along_y(y - ROD_BORE_DEEP, y)
    spacer = spacer.cut(bore.center(cx, cz).pushPoints(rods).circle(ROD_BORE_D / 2).extrude(d))
spacer = spacer.cut(cq.Workplane("XY", origin=(0, 0, cz - HEIGHT)).pushPoints([(cx, y) for y in CROSS_Y])
                    .circle(CROSS_D / 2).extrude(2 * HEIGHT))

result = spacer
