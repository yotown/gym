"""Open Duck Mini v2 antenna holder (left), written from its STEP: interfaces exact, the body simple.
right_antenna_holder is this part mirrored across the robot's middle (y = 0).

A cup on the antenna servo: a D-shaped base (round, cut flat at its back) on a short tube round the
servo's shaft, and a D-shaped wall standing on it -- the antenna's socket. The shaft's screw through the
base; a fine hole for the antenna's wire.

Frame: the cup's own, (u, v, w) in mm: w along the antenna's axis, u out through the flat back, origin
on the axis (FRAME places it in the vendor's frame).
"""

import cadquery as cq

FRAME = dict(origin=(-28.652, -34.743, 105.672), u=(0.9648, 0.2551, 0.0644), w=(-0.2631, 0.9354, 0.2362))   # measured

# -- interfaces -- fixed ----------------------------------------------------------------------------
SHAFT_BORE_D = 5.05                        # the tube round the antenna servo's shaft: bore,
SHAFT_W = (98.924, 101.994)                # w from-to
SHAFT_SCREW_D = 2.7                        # the screw through the base into the shaft
WIRE_AT = (-56.406, 91.105, 23.006)        # the antenna wire's hole, in the vendor's frame: a point,  # measured
WIRE_DIR = (0.0, -0.2448, 0.9696)          # its direction,  # measured
WIRE_D = 1.8
SOCKET_R = 18.6155                         # the antenna's socket: the cup's inside r

# -- body: free -------------------------------------------------------------------------------------
SHAFT_TUBE_D = 9.05                        # the shaft's tube outside
BASE = (101.994, 103.994)                  # w from-to
WALL_TOP = 108.994
WALL = 2.0                                 # the cup's wall, outside the socket
BACK = (3.0, 5.0)                          # the flat back wall: u from-to

CUP_R = SOCKET_R + WALL


def prism(r, flat_u, w0, w1):
    wp = cq.Workplane("XY", origin=(0, 0, w0))
    return wp.circle(r).extrude(w1 - w0).intersect(wp.center(flat_u - 2 * r, 0).rect(4 * r, 4 * r).extrude(w1 - w0))


b0, b1 = BASE
cup = prism(CUP_R, BACK[1], b0, b1)
cup = cup.union(prism(CUP_R, BACK[1], b1, WALL_TOP).cut(prism(SOCKET_R, BACK[0], b1, WALL_TOP + 1)))
(bore, outside), (t0, t1), screw = (SHAFT_BORE_D, SHAFT_TUBE_D), SHAFT_W, SHAFT_SCREW_D
cup = cup.union(cq.Workplane("XY", origin=(0, 0, t0)).circle(outside / 2).extrude(t1 - t0 + 0.01))
cup = cup.cut(cq.Workplane("XY", origin=(0, 0, t0 - 1)).circle(bore / 2).extrude(t1 - t0 + 1.5))
cup = cup.cut(cq.Workplane("XY", origin=(0, 0, t0)).circle(screw / 2).extrude(b1 - t0 + 1))

u, w = cq.Vector(*FRAME["u"]), cq.Vector(*FRAME["w"])
placed = cq.Workplane(obj=cup.val().transformShape(cq.Plane(origin=FRAME["origin"], xDir=u, normal=w).rG))
p, direction, d = WIRE_AT, WIRE_DIR, WIRE_D
wire = cq.Solid.makeCylinder(d / 2, 200, cq.Vector(*p) + cq.Vector(*direction) * 30, cq.Vector(*direction))
result = placed.cut(cq.Workplane(obj=wire))
