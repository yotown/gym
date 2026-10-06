"""LeRobot humanoid shoulder link (shoulder 2), written from its STEP: interfaces exact, the body simple.

Two interfaces, each in its own frame. The BASE turns on the shoulder's vertical axis: a ring with a
spigot below, a bore, six counterbored screws, two pins and six tapped holes. The FLANGE, out along the
arm and tilted down, carries the next joint: a spigot, a bore, six counterbored M3s and six tapped
holes; behind it a d58 cavity ends at a wall with three M3s screwed from below.

Between them the arm: a side profile (a flat underside blending into the flange, a long round over the
top) across the base ring's width, trimmed by two planes tangent to the flange's rim.

Frames: the STEP's (mm), z up. The base's axis is vertical through BASE_AT; the arm lies in the vertical
plane through it at ARM_DEG round from x. The flange's axis is in that plane, FLANGE_TILT from vertical,
its spigot's top centre at FLANGE_AT (along the arm, across it, up); its patterns are clocked from the
arm's top by FLANGE_CLOCK.
"""

import math

import cadquery as cq

# -- interfaces -- fixed ----------------------------------------------------------------------------
# the base, on the shoulder's axis
BASE_AT = (-0.468, -0.075)                 # the shoulder's axis (x, y), vertical  # measured
BASE_FACE_Z = -2.0                         # the base's face on the joint below
SPIGOT_D = 45.6                            # the centring spigots, both ends; not in the model: the bearings the spigots centre in
BASE_SPIGOT_H = 1.0                        # under the base's face; not in the model: the bearing the spigot centres in
BORE_D = 43.0                              # through both ends; not in the model: what passes through
BASE_BOLT_CIRCLE_D = 50.0
BASE_BOLT_FIRST_DEG = 0.0                  # from x
BASE_BOLT_COUNT = 6
BASE_BOLT_D = 2.5                          # tapped, from the face up to BASE_BOLT_DEEP
BASE_BOLT_HEAD_D = 6.5                     # counterbored from below ...
BASE_BOLT_HEAD_SEAT = 6.0                  # ... to this far above the face
BASE_TAP_CIRCLE_D = 60.0
BASE_TAP_FIRST_DEG = -22.5
BASE_TAP_COUNT = 6
BASE_TAP_D = 2.9
BASE_PIN_DEG = (15.0, 195.0)               # dowels on the bolt circle
BASE_PIN_D = 3.0
# the flange, out along the arm
ARM_DEG = 9.023                            # the arm's vertical plane, round from x  # measured
FLANGE_ALONG = 126.651                     # the flange spigot's top centre: along the arm from the axis,  # measured
FLANGE_ACROSS = 0.066                      # across it,  # measured
FLANGE_UP = 58.279                         # and up  # measured
FLANGE_TILT_DEG = 52.246                   # its axis from vertical, out along the arm  # measured
FLANGE_CLOCK_DEG = -0.461                  # its patterns' zero, from the arm's top  # measured
FLANGE_SPIGOT_H = 1.2                      # over the flange's face
FLANGE_BOLT_CIRCLE_D = 50.0
FLANGE_BOLT_FIRST_DEG = 15.0
FLANGE_BOLT_COUNT = 6
FLANGE_BOLT_D = 3.3                        # M3 through
FLANGE_BOLT_HEAD_D = 6.5
FLANGE_BOLT_HEAD_SEAT = 11.2               # below the spigot's top; not in the model: the screws
FLANGE_TAP_CIRCLE_D = 60.0
FLANGE_TAP_FIRST_DEG = 45.0
FLANGE_TAP_COUNT = 6
FLANGE_TAP_D = 2.9
CAVITY_D = 58.0                            # behind the flange, for the next joint's motor; not in the model: the next joint's motor body
CAVITY_FLOOR = 76.2                        # below the spigot's top
FLOOR_T = 5.0                              # the floor; three M3 up through it; not in the model: the screws
FLOOR_BOLT_CIRCLE_D = 38.0
FLOOR_BOLT_DEG = (-90.0, 180.0, 90.0)
FLOOR_BOLT_D = 3.3
FLOOR_BOLT_HEAD_D = 6.5
FLANGE_T = 23.0                            # under the spigot

# -- body: free -------------------------------------------------------------------------------------
BASE_BOLT_DEEP = 10.5
BASE_TAP_DEEP = 5.0
BASE_PIN_DEEP = 10.5
FLANGE_TAP_DEEP = 26.2
BASE_R = 35.0                              # the base ring, and the arm's half width
BASE_TOP_Z = 28.0
ARM_SIDE = 35.0                            # the arm's side profile, across: to this side,
ARM_OTHER_SIDE = 34.9                      # and to the other  # measured
FLANGE_R = 32.5                            # the flange plate
UNDER_BLEND_AT = (51.49, -41.031)          # the underside's round into the flange: centre (along, up)  # measured
UNDER_BLEND_R = 39.031                     # measured
TOP_BLEND_AT = (0.278, 128.0)              # the top's round: centre (along, up)  # measured
TOP_BLEND_R = 100.0
SIDE_LEAN_DEG = 4.14                       # the sides: tangent to the flange's rim, leaning in to it  # measured
OTHER_SIDE_LEAN_DEG = 4.278                # measured
HULL_H = 70.0                              # the sides run this far up from the flange's axis
SIDE_PAST = 10.0                           # the profile reaches this far past the rim under the arm
WINDOW_WIDE = 100.0                        # the cavity open underneath
WINDOW_DEEP = 60.0
RELIEF_D = 57.0                            # the bore opened above the base,
RELIEF_FROM_Z = 8.0                        # from
RELIEF_TO_Z = 45.0                         # to

Vec = cq.Vector
zv = Vec(0, 0, 1)
az, tilt = math.radians(ARM_DEG), math.radians(FLANGE_TILT_DEG)
v_dir = Vec(math.cos(az), math.sin(az), 0)     # along the arm, in plan
u_dir = zv.cross(v_dir)                            # across it
c1 = Vec(*BASE_AT, 0)
flange_dir = v_dir * math.sin(tilt) + zv * math.cos(tilt)   # the flange's axis, out of its face
w_dir = flange_dir.cross(u_dir)                           # across that axis, towards the arm's top
p2 = c1 + v_dir * FLANGE_ALONG + u_dir * FLANGE_ACROSS + zv * FLANGE_UP
back = FLANGE_SPIGOT_H + FLANGE_T          # the flange plate's back, below the spigot's top


def cyl(p, axis, d, t0, t1):
    return cq.Solid.makeCylinder(d / 2.0, t1 - t0, p + axis * t0, axis)


def on_base(c, deg):
    a = math.radians(deg)
    return c1 + Vec(c / 2 * math.cos(a), c / 2 * math.sin(a), 0)


def on_flange(c, deg):
    a = math.radians(FLANGE_CLOCK_DEG + deg)
    return p2 + w_dir * (c / 2 * math.cos(a)) + u_dir * (c / 2 * math.sin(a))


# ---- the arm: its side profile in the arm's plane (along, up), across the base ring's width
dx, dz = flange_dir.dot(v_dir), flange_dir.z
wx, wz = -dz, dx                           # across the flange's axis, in that plane
ax, az_ = FLANGE_ALONG, FLANGE_UP
(clx, clz), r_low = UNDER_BLEND_AT, UNDER_BLEND_R
(ctx, ctz), r_top = TOP_BLEND_AT, TOP_BLEND_R
end_low = (clx + r_low * dx, clz + r_low * dz)
m = math.hypot(dx, 1.0 + dz)
mid_low = (clx + r_low * dx / m, clz + r_low * (1.0 + dz) / m)
h = FLANGE_SPIGOT_H
under_rim = (ax - h * dx - (FLANGE_R + SIDE_PAST) * wx, az_ - h * dz - (FLANGE_R + SIDE_PAST) * wz)
over_rim = (ax - h * dx + FLANGE_R * wx, az_ - h * dz + FLANGE_R * wz)
top_start = (ctx - r_top * wx, ctz - r_top * wz)
m = math.hypot(dz, 1.0 + dx)
mid_top = (ctx + r_top * dz / m, ctz - r_top * (1.0 + dx) / m)
top_end = (ctx, ctz - r_top)
side = cq.Plane(origin=c1 + u_dir * ARM_SIDE, xDir=v_dir, normal=u_dir * -1.0)
arm = (cq.Workplane(side).moveTo(0, BASE_FACE_Z).lineTo(clx, BASE_FACE_Z)
       .threePointArc(mid_low, end_low).lineTo(*under_rim).lineTo(*over_rim).lineTo(*top_start)
       .threePointArc(mid_top, top_end).lineTo(0, BASE_TOP_Z).close()
       .extrude(ARM_SIDE + ARM_OTHER_SIDE))


# ---- trimmed along the flange's axis by its two sides, each tangent to the flange's rim
def tangent(lean, sign):
    """A side's tangent point on the rim and where it is at HULL_H (in the flange's (-u_dir, w_dir) plane)."""
    nu, nw = sign * math.cos(math.radians(lean)), -math.sin(math.radians(lean))
    return (FLANGE_R * nu, FLANGE_R * nw), (FLANGE_R - nw * HULL_H) / nu


(rt, ry), (lt, ly) = tangent(SIDE_LEAN_DEG, 1), tangent(OTHER_SIDE_LEAN_DEG, -1)
flange_plane = cq.Plane(origin=p2 - flange_dir * (FLANGE_SPIGOT_H - 1.0), xDir=u_dir * -1.0, normal=flange_dir * -1.0)
hull = (cq.Workplane(flange_plane).moveTo(-rt[0], rt[1]).lineTo(-ry, HULL_H).lineTo(-ly, HULL_H)
        .lineTo(-lt[0], lt[1]).threePointArc((0.0, -FLANGE_R), (-rt[0], rt[1])).close()
        .extrude(201.0))
body = arm.intersect(hull)

# ---- the base ring (its half away from the arm; the arm makes the rest)
ring_plane = cq.Plane(origin=c1 + zv * BASE_FACE_Z, xDir=v_dir, normal=zv)
body = body.union(cq.Workplane(ring_plane).moveTo(0, -BASE_R).threePointArc((-BASE_R, 0), (0, BASE_R)).close()
                  .extrude(BASE_TOP_Z - BASE_FACE_Z))

# ---- the cavity behind the flange, open underneath; the base's bore opened above it
window_plane = cq.Plane(origin=p2 - flange_dir * back, xDir=u_dir * -1.0, normal=flange_dir * -1.0)
body = body.cut(cq.Workplane(window_plane).center(0, -WINDOW_DEEP / 2).rect(WINDOW_WIDE, WINDOW_DEEP).extrude(CAVITY_FLOOR - back))
body = body.cut(cyl(p2, flange_dir * -1.0, CAVITY_D, back, CAVITY_FLOOR))
body = body.cut(cyl(c1, zv, RELIEF_D, RELIEF_FROM_Z, RELIEF_TO_Z))

# -- interfaces, cut last -------------------------------------------------------------------------
below = BASE_FACE_Z - BASE_SPIGOT_H - 1.0  # under everything at the base
body = body.union(cyl(c1, zv, SPIGOT_D, BASE_FACE_Z - BASE_SPIGOT_H, BASE_FACE_Z))
body = body.union(cyl(p2, flange_dir * -1.0, SPIGOT_D, 0.0, FLANGE_SPIGOT_H))
body = body.cut(cyl(p2, flange_dir * -1.0, BORE_D, -1.0, back + 0.5))
body = body.cut(cyl(c1, zv, BORE_D, below, RELIEF_FROM_Z))

for i in range(BASE_BOLT_COUNT):
    p = on_base(BASE_BOLT_CIRCLE_D, BASE_BOLT_FIRST_DEG + 360.0 / BASE_BOLT_COUNT * i)
    body = body.cut(cyl(p, zv, BASE_BOLT_HEAD_D, below, BASE_FACE_Z + BASE_BOLT_HEAD_SEAT))
    body = body.cut(cyl(p, zv, BASE_BOLT_D, BASE_FACE_Z + BASE_BOLT_HEAD_SEAT, BASE_FACE_Z + BASE_BOLT_DEEP))
for i in range(BASE_TAP_COUNT):
    p = on_base(BASE_TAP_CIRCLE_D, BASE_TAP_FIRST_DEG + 360.0 / BASE_TAP_COUNT * i)
    body = body.cut(cyl(p, zv, BASE_TAP_D, below, BASE_FACE_Z + BASE_TAP_DEEP))
for a in BASE_PIN_DEG:
    body = body.cut(cyl(on_base(BASE_BOLT_CIRCLE_D, a), zv, BASE_PIN_D, below, BASE_FACE_Z + BASE_PIN_DEEP))

out = flange_dir * -1.0                           # into the part from the flange
for i in range(FLANGE_BOLT_COUNT):
    p = on_flange(FLANGE_BOLT_CIRCLE_D, FLANGE_BOLT_FIRST_DEG + 360.0 / FLANGE_BOLT_COUNT * i)
    body = body.cut(cyl(p, out, FLANGE_BOLT_HEAD_D, -1.0, FLANGE_BOLT_HEAD_SEAT))
    body = body.cut(cyl(p, out, FLANGE_BOLT_D, FLANGE_BOLT_HEAD_SEAT, back + 0.5))
for i in range(FLANGE_TAP_COUNT):
    p = on_flange(FLANGE_TAP_CIRCLE_D, FLANGE_TAP_FIRST_DEG + 360.0 / FLANGE_TAP_COUNT * i)
    body = body.cut(cyl(p, out, FLANGE_TAP_D, -1.0, FLANGE_TAP_DEEP))
for a in FLOOR_BOLT_DEG:
    p = on_flange(FLOOR_BOLT_CIRCLE_D, a)
    body = body.cut(cyl(p, out, FLOOR_BOLT_D, CAVITY_FLOOR - 0.5, CAVITY_FLOOR + FLOOR_T))
    body = body.cut(cyl(p, out, FLOOR_BOLT_HEAD_D, CAVITY_FLOOR + FLOOR_T, 115.0))

result = body
