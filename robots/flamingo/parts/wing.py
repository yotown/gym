"""Flamingo wing: a yoke on the wing servo's horn and idler, and the blade it carries.

The yoke is the Duck's head-pitch yoke in kind: a plate on the horn and one on the idler, each held by the
four horn screws, joined by a bridge past the case's near end. The blade runs out from the bridge, swept
back, thin, with a spar along its leading edge and its trailing edge scalloped into feathers. At the joint's
zero it lies level, out from the body.

Frame: the servo's own (shared.py): x = back (the blade runs out along -x), y = across (the blade's
thickness), z = into (its chord: the leading edge at -z, the front of the robot).
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)
F = S.F

# -- interfaces -- fixed ----------------------------------------------------------------------------
HORN_HOLES, IDLER_HOLES = S.HORN.points(), S.IDLER.points()   # (back, across)
SCREW = S.CLEARANCE[F.horn_thread]
SCREW_GRIP = 2.0                           # under each horn screw's head, to the horn
IDLER_FACE = F.idler_face                  # the idler's face, into from the horn's
NEAR = F.case_near                         # the case's near end, ahead of the axis

# -- body: free -------------------------------------------------------------------------------------
TY = 3.5                                   # each yoke plate
R = 11.5                                   # the plates' round ends about the axis: inside the cradle's start (17)
BORE_D = 7.0                               # a key to the horn's own screw, through each plate's middle
GAP = 2.0                                  # the bridge clears the case's near end by this
BRIDGE = 4.0
HALF_ACROSS = 11.5                         # the yoke's width
SPAN = 135.0                               # the blade, from the bridge out: wide enough to read beside the head
BLADE_T = 3.0
SPAR_T, SPAR_W = 6.0, 8.0                  # its leading-edge spar: thickness, width
FEATHER_R = 7.0
z0, z1 = -TY, IDLER_FACE + TY
TE = z1 + 14.0                             # the trailing edge at the root (the chord runs from z0 - 6 to here)
b0 = -(NEAR + GAP)                         # the bridge, back from the axis: b0 - BRIDGE .. b0
root = b0 - BRIDGE
# the blade's outline (back, into): swept back, its tip rounded
BLADE = [(root + 1, z0 - 6), (root - SPAN + 8, 16.0), (root - SPAN, 26.0), (root - SPAN + 6, 36.0),
         (root - SPAN * 0.45, TE), (root + 1, TE)]


def plate(za, zb):
    """A yoke plate: round about the axis, running out to the bridge."""
    wp = cq.Workplane("XY", origin=(0, 0, za))
    return wp.circle(R).extrude(zb - za).union(wp.center((b0 + 0) / 2 - 2, 0).rect(-b0 + 4, 2 * HALF_ACROSS).extrude(zb - za))


wing = plate(z0, 0).union(plate(IDLER_FACE, z1))
wing = wing.union(cq.Workplane("XY").box(BRIDGE, 2 * HALF_ACROSS, z1 - z0, centered=False).translate((root, -HALF_ACROSS, z0)))
side = cq.Workplane("XZ")                  # (back, into) on y = 0; XZ's normal is -y, so both ways
blade = side.polyline(BLADE).close().extrude(BLADE_T / 2, both=True)
spar = side.polyline([(root + 1, z0 - 6), (root - SPAN + 8, 16.0), (root - SPAN + 8, 16.0 + SPAR_W),
                      (root + 1, z0 - 6 + SPAR_W)]).close().extrude(SPAR_T / 2, both=True)
wing = wing.union(blade).union(spar)
for i in range(3):                         # the feathers: scallops along the trailing edge
    t = 0.25 + 0.2 * i
    bx = root - SPAN * 0.45 * t - SPAN * 0.55 * t
    te = TE + (36.0 - TE) * max(0.0, (-(bx - root) - SPAN * 0.45) / (SPAN * 0.55))   # the trailing edge there
    wing = wing.cut(side.center(bx, te + FEATHER_R * 0.55).circle(FEATHER_R).extrude(SPAR_T, both=True))
# the horn screws and the middle bores, cut last
for za, holes, d in ((0.0, HORN_HOLES, -1), (IDLER_FACE, IDLER_HOLES, 1)):
    wp = cq.Workplane(cq.Plane(origin=(0, 0, za), xDir=(1, 0, 0), normal=(0, 0, d)))
    wing = wing.cut(wp.pushPoints(holes).circle(SCREW.hole_d / 2).extrude(TY + 1))
    wing = wing.cut(wp.workplane(offset=SCREW_GRIP).pushPoints(holes).circle(SCREW.head_d / 2).extrude(TY))
    wing = wing.cut(wp.circle(BORE_D / 2).extrude(TY + 1))
result = wing
