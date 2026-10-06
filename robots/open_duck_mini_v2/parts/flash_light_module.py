"""Open Duck Mini v2 flash light module, written from its STEP: interfaces exact, the body simple.

A barrel round the flash's axis running down in straight flanks to its face on the head, with four bosses
for the screws that hold it there (their heads counterbored from above); in the barrel's front a conical seat for the reflector interface,
through its back a hole for the light's wires. The base's ends rounded, the barrel's ends chamfered.

Frame: the vendor's (mm): the axis runs along x through AXIS (y, z); the base's face onto the head is
the plane MOUNT (its normal, in (y, z), and its level along it).
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
# this part is not in the model: what it fits is declared
MOUNT_DEG = 20.0                           # the base's face onto the head: its normal turned from +y towards +z,  # measured
MOUNT_LEVEL = 130.553                      # its level (the head's side by the eyes); not in the model: this part  # measured
SCREW_X = (90.0, 110.0)                    # into the head's side: x,
SCREW_ACROSS = 17.0                        # +- across from the axis,
SCREW_D = 2.7
SCREW_HEAD_D = 5.5                         # counterbored from above,
SCREW_HEAD_LEVEL = 133.053                 # down to this level; not in the model: this part
SEAT_FRONT_D = 23.0                        # the reflector interface's seat in the front: its cone, at the mouth
SEAT_BACK_D = 21.67                        # at its back; not in the model: the reflector interface  # measured
SEAT_X = 101.3                             # from x; not in the model: the reflector interface
FRONT_X = 114.0                            # to the barrel's front face, its mouth; not in the model: the reflector interface
WIRES_D = 4.0                              # the wires' hole, through the back along the axis

# -- body: free -------------------------------------------------------------------------------------
WIRES_X = 87.0                             # the wires' hole, from x
BACK_X = 86.0                              # the barrel's back face
BARREL_D = 26.0
CHAMFER = 0.5
FOOT = (-16.5, 16.5)                       # the face on the head: from-to across, from the axis  # measured
BOSS_D = 8.0                               # each screw's boss,
BOSS_LEVEL = 136.35                        # up to this level

ay, az = S.FLASH_AXIS_Y, S.FLASH_AXIS_Z
deg, mount = MOUNT_DEG, MOUNT_LEVEL
n = (math.cos(math.radians(deg)), math.sin(math.radians(deg)))      # the base's normal, in (y, z)
t = (-n[1], n[0])                                                    # across the base
axis_u, axis_t = n[0] * ay + n[1] * az, t[0] * ay + t[1] * az
x0, x1 = BACK_X, FRONT_X


def at(u, tt):
    """(y, z) of the point at level u along the normal and tt across."""
    return (u * n[0] + tt * t[0], u * n[1] + tt * t[1])


barrel = cq.Workplane("YZ", origin=(x0, 0, 0)).center(ay, az).circle(BARREL_D / 2).extrude(x1 - x0).faces("<X or >X").edges().chamfer(CHAMFER)
# the body: the barrel and its flanks, tangent from the foot's ends to the barrel


def tangent(p, c, r, side):
    """The point where a line from p touches the circle (c, r), on the given side."""
    dy, dz = p[0] - c[0], p[1] - c[1]
    d = math.hypot(dy, dz)
    a = math.atan2(dz, dy) + side * math.acos(r / d)
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


f0, f1 = (at(mount, axis_t + f) for f in FOOT)
body = [f0, tangent(f0, (ay, az), BARREL_D / 2, 1), tangent(f1, (ay, az), BARREL_D / 2, -1), f1]
module = barrel.union(cq.Workplane("YZ", origin=(x0, 0, 0)).polyline(body).close().extrude(x1 - x0))
xs, across, d, (cb, cb_level), (boss, boss_level) = SCREW_X, SCREW_ACROSS, SCREW_D, (SCREW_HEAD_D, SCREW_HEAD_LEVEL), (BOSS_D, BOSS_LEVEL)
for x in xs:
    for s in (1, -1):
        p = at(mount, axis_t + s * across)
        module = module.union(cq.Workplane().add(cq.Solid.makeCylinder(boss / 2, boss_level - mount, cq.Vector(x, *p), cq.Vector(0, *n))))
# nothing below the mount face
below = [at(mount, axis_t - 40), at(mount, axis_t + 40), at(mount - 40, axis_t + 40), at(mount - 40, axis_t - 40)]
module = module.cut(cq.Workplane("YZ", origin=(x0 - 1, 0, 0)).polyline(below).close().extrude(x1 - x0 + 2))

(sd0, sd1), sx = (SEAT_BACK_D, SEAT_FRONT_D), SEAT_X
module = module.cut(cq.Workplane().add(cq.Solid.makeCone(sd0 / 2, sd1 / 2, x1 - sx, cq.Vector(sx, ay, az), cq.Vector(1, 0, 0))))
module = module.cut(cq.Workplane().add(cq.Solid.makeCylinder(sd1 / 2, 1, cq.Vector(x1 - 0.01, ay, az), cq.Vector(1, 0, 0))))
wd, wx = WIRES_D, WIRES_X
module = module.cut(cq.Workplane("YZ", origin=(wx, 0, 0)).center(ay, az).circle(wd / 2).extrude(sx - wx + 0.01))
for x in xs:
    for s in (1, -1):
        p = at(mount - 5, axis_t + s * across)
        hole = cq.Solid.makeCylinder(d / 2, 30, cq.Vector(x, *p), cq.Vector(0, *n))
        head_from = at(cb_level, axis_t + s * across)
        head = cq.Solid.makeCylinder(cb / 2, 30, cq.Vector(x, *head_from), cq.Vector(0, *n))
        module = module.cut(cq.Workplane().add(hole)).cut(cq.Workplane().add(head))

result = module
