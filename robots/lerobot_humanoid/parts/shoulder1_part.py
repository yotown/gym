"""Robot shoulder elbow: two d35 bearing-bore bosses joined at 84.2 degrees. One boss is vertical along +z
on axis (-0.329, -0.173) with its top at z 24.6. The other boss is tilted along
d = (-0.6707, 0.7348, 0.1008) through (-9.451, 9.632, -41.675) with its top at t 25.
The two axes cross at crossing. Above crossing and short of crossing, each boss is a plain cylinder (the arms). Past crossing, the
elbow joint is the region common to both infinite cylinders. A sphere about crossing clips its outer corner, and
the sphere passes where both cylinder faces end (z -56.861 and t -27.289, each 13.83 mm past crossing).
Each boss has a 5 mm top plate with six M3 holes on an r 13.5 circle. Each hole is d3.4 through the plate
over a long d6.5 bore that opens at the far side of the part. Each boss also has three d3.4 tapped holes,
10 mm deep, on an r 12.23 circle. A 25 mm wide wedge-shaped notch is cut into the +u side of the vertical
boss above the tilted boss. It is bounded by planes 33 (floor), 31 (ceiling), 1/32/0 (wall) and 29/30 (sides).
Frame: the STEP's own frame, in mm.
Approximated: the free-form corner faces are modelled as a sphere through the ends of both cylinder
faces. Not reproduced: the short d3.4 stubs (about 23 mm2 each) deep inside the part."""

import math

import cadquery as cq

# -- interfaces -- fixed ----------------------------------------------------------------------------
# the vertical boss, on the shoulder's axis
VERTICAL_AXIS_XY = (-0.329, -0.173)        # its axis (x, y), along z  # measured
VERTICAL_TOP_Z = 24.6                      # its top: the next part on it
# the tilted boss, on the next joint's axis
TILTED_AXIS_AT = (-9.451, 9.632, -41.675)  # a point on its axis  # measured
TILTED_AXIS_DIR = (-0.6707, 0.7348, 0.1008)   # out of its top  # measured
TILTED_TOP = 25.0                          # its top, along its axis from that point
# each top: six screws through, counterbored from below; three tapped
BOLT_CIRCLE_D = 27.0
BOLT_COUNT = 6
BOLT_D = 3.4
BOLT_HEAD_D = 6.5                          # each a long bore from the far side of the part,
BOLT_HEAD_SEAT = 5.0                       # up to this far under the top
VERTICAL_BOLT_FIRST_DEG = 0.0              # from x
TILTED_BOLT_FIRST_DEG = 41.8               # from the plane both axes lie in  # measured
TAP_CIRCLE_D = 24.46
TAP_COUNT = 3
TAP_D = 3.4
TAP_DEEP = 10.0
VERTICAL_TAP_FIRST_DEG = 30.0
TILTED_TAP_FIRST_DEG = 11.8                # measured

# -- body: free -------------------------------------------------------------------------------------
BOSS_D = 35.0                              # both bosses
CORNER_Z = -56.861                         # past the axes' crossing both bosses meet in a ball, through here  # measured
NOTCH_W = 25.0                             # a notch in the vertical boss over the tilted one: wide,
NOTCH_FROM = -12.86                        # from here across the plane of the axes,
NOTCH_FLOOR = ((0.0679, -0.0744, 0.9949), -24.8)     # between its floor,  # measured
NOTCH_CEILING = ((-0.2544, 0.2788, -0.926), 12.184)  # its ceiling  # measured
NOTCH_WALL = ((-0.6707, 0.7348, 0.1008), 9.861)      # and its wall (each a normal and a level)  # measured
NOTCH_REACH = 60.0                         # out past the boss

Vec = cq.Vector
zv = Vec(0, 0, 1)
d2 = Vec(*TILTED_AXIS_DIR).normalized()
s_dir = zv.cross(d2).normalized() * -1.0   # across the plane of both axes
u_dir = zv.cross(s_dir)                    # horizontal, in that plane
n_dir = s_dir.cross(d2).normalized()       # across the tilted axis, in that plane
v_c = Vec(*VERTICAL_AXIS_XY, 0)
t_a = Vec(*TILTED_AXIS_AT)


def cyl(d, p, axis, a, b):
    return cq.Solid.makeCylinder(d / 2, b - a, p + axis * a, axis)


# where the tilted axis meets the vertical one
t_o = -u_dir.dot(t_a - v_c) / u_dir.dot(d2)
o_z = t_a.z + d2.z * t_o
crossing = Vec(v_c.x, v_c.y, o_z)
ball_r = math.sqrt((BOSS_D / 2) ** 2 + (o_z - CORNER_Z) ** 2)

# each boss from the crossing to its top; past the crossing, where both meet, clipped by the ball
v_arm = cyl(BOSS_D, v_c, zv, o_z, VERTICAL_TOP_Z)
t_arm = cyl(BOSS_D, t_a, d2, t_o, TILTED_TOP)
v_long = cyl(BOSS_D, v_c, zv, o_z - 40.0, VERTICAL_TOP_Z)
t_long = cyl(BOSS_D, t_a, d2, t_o - 40.0, TILTED_TOP)
ball = cq.Workplane("XY", origin=(crossing.x, crossing.y, crossing.z)).sphere(ball_r).val()
body = v_arm.fuse(t_arm).fuse(v_long.intersect(t_long).intersect(ball))


# the notch: in the plane of the axes, between its floor, ceiling and wall
def line(plane):
    n, level = plane
    n = Vec(*n).normalized()
    return (n.dot(u_dir), n.dot(zv), level - NOTCH_FROM * n.dot(s_dir))


def meet(l1, l2):
    a1, b1, c1 = l1
    a2, b2, c2 = l2
    det = a1 * b2 - a2 * b1
    return ((c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det)


def at_u(l, u):
    a, b, c = l
    return (u, (c - a * u) / b)


floor, ceil, wall = line(NOTCH_FLOOR), line(NOTCH_CEILING), line(NOTCH_WALL)
pts = [meet(wall, floor), meet(wall, ceil), at_u(ceil, NOTCH_REACH), at_u(floor, NOTCH_REACH)]
tools = [cq.Workplane(cq.Plane(origin=s_dir * NOTCH_FROM, xDir=u_dir, normal=s_dir)).polyline(pts).close().extrude(NOTCH_W).val()]

# -- interfaces, cut last -------------------------------------------------------------------------
for at, axis, top, x_dir, y_dir, bolt_first, tap_first, far in (
        (v_c, zv, VERTICAL_TOP_Z, Vec(1, 0, 0), Vec(0, 1, 0), VERTICAL_BOLT_FIRST_DEG, VERTICAL_TAP_FIRST_DEG, -90.0),
        (t_a, d2, TILTED_TOP, s_dir, n_dir, TILTED_BOLT_FIRST_DEG, TILTED_TAP_FIRST_DEG, -80.0)):
    on = lambda r, deg: at + x_dir * (r * math.cos(math.radians(deg))) + y_dir * (r * math.sin(math.radians(deg)))   # noqa: E731
    for k in range(BOLT_COUNT):
        c = on(BOLT_CIRCLE_D / 2, bolt_first + 360.0 / BOLT_COUNT * k)
        tools.append(cyl(BOLT_HEAD_D, c, axis, far, top - BOLT_HEAD_SEAT))
        tools.append(cyl(BOLT_D, c, axis, top - BOLT_HEAD_SEAT - 1.0, top + 1.0))
    for k in range(TAP_COUNT):
        c = on(TAP_CIRCLE_D / 2, tap_first + 360.0 / TAP_COUNT * k)
        tools.append(cyl(TAP_D, c, axis, top - TAP_DEEP, top + 1.0))

body = body.cut(*tools).clean()
result = cq.Workplane("XY").add(body)
