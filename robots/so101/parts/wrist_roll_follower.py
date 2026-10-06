"""SO-101 wrist roll follower (the gripper's fixed jaw), written from its STEP: the interfaces exact, the body free.

Frame: the vendor's (Wrist_Roll_Follower_SO101.step / Menagerie STL, mm): z up the wrist-roll
axis; the gripper servo lies on the floor with its length along x and its axis along -y (its horn
on the +y side, where the moving jaw is); the fixed finger rises at the back (x < 0).
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # SO-101's shared values (../shared.py): its servo, its screws
SERVO, SERVO_SCREW = S.SERVO, S.SERVO_SCREW

# -- interfaces: from the robot model (so101.xml) and the catalogue (feetech_sts3215) -- fixed ------
ROLL_AXIS = (0.0, -0.218)                  # the wrist_roll axis (x, y), along z
HORN_FACE_Z = 0.95                         # the roll servo's horn face: the follower's boss sits on it (the vendor's STEP)  # measured
HORN_CLOCK_DEG = -2.8                      # the model clocks the horn 2.8 deg off the servo's 45
HORN_SCREW_D, HORN_SCREW_HEAD_D, HORN_SCREW_SEAT = 3.2, 6.0, 3.0   # measured
HUB_ACCESS_D = 6.4                         # to the horn's centre screw  # measured
SEAT_RECESS = (24.6, 2.0)                  # a round recess in the floor's top over the boss: diameter, depth  # measured
GRIP_Y, GRIP_Z = -0.318, 24.35             # the gripper STS3215's origin (y, z): its length along x,
# the case's raised faces beside the back walls, each a recess (the vendor's servo mesh)  # measured
CASE_FACE_POS = dict(x=(-10.7, 20.0), z=(14.6, 34.1), y=17.7)
CASE_FACE_NEG = dict(x=(-15.5, 20.0), z=(16.8, 31.9), y=-17.45)
SERVO_SCREW_Z = (14.1, 34.6)               # the servo's back tabs: two screws through each wall
SERVO_SCREW_X = {1: -12.6, -1: -8.8}       # in the +y and the -y wall
BACK_HALF_WIDTH, FLOOR_HALF_WIDTH = 15.95, 24.0
BLOCK_FRONT_X = -15.0                      # the back block, the finger's root
WALL_THICKNESS = 8.0                       # the side walls, clear of the servo's output end
WALL_FRONT = {1: (0.94, 0.342, 7.914), -1: (0.894, 0.447, 18.3)}   # each wall's front edge, leaning back: a x + b z up to c  # measured
CABLE_D = 10.0                             # through the back block, along x
FINGER_HOLE_D, FINGER_HOLE_FROM, FINGER_HOLE_STEP = 1.5, (-27.46, 50.74), (3.42, 9.4)   # five fixing holes up the finger

# -- body: free ------------------------------------------------------------------------------------
GRIP_X = 7.7                               # its origin along x, its half length: its pocket is clear of the servo there, so free
BLOCK_TOP = 38.0                           # the back block's top
HORN_BOSS_D = 24.0                         # the boss the horn is screwed to
BOSS_TAB = (-12.0, 4.4)                    # the boss runs back to this x, this wide (half), cut 45 deg into the circle  # measured
TAB_CHAMFER = ((-11.0, 0.95), (-17.0, 5.95))   # its underside rises from the first point to the second, clear of the yoke  # measured
FLOOR_BOTTOM = 5.95
BACK_X, FRONT_X = -35.2, 29.8
TAPER_FROM_X, TAPER_TO_X = -25.2, -12.0    # the floor widens from the back block
FRONT_CHAMFER, CORNER_R = 9.8, 3.0
NUT_POCKETS = dict(x=(-5.0, 3.1), z=24.35, across_flats=5.6, depth=3.3, hole_d=3.2)   # two M3 nuts in the -y wall's inside, their screws out through it  # measured
CAP_TO_X, CAP_THICKNESS = 1.95, 1.25       # a cap over the servo's back
CAP_HALF_WIDTH = 21.0                      # measured
ROOT_TOP, ROOT_HALF_WIDTH = 46.07, 13.6   # a slab on the block, under the finger
# the finger, the fixed jaw: a straight back edge, a stepped front, a rounded top; it narrows evenly upward
# (its gripping pad sets the grasp: the jaw gap at each angle is checked by the sweep's --grip)
GRIP_FACE_X = -7.9          # the gripping pad: the finger's front face from the pad's foot to the top  # measured
FINGER_BACK = ((-35.2, 44.3), (-15.0, 100.0))   # the back edge, a straight line  # measured
FINGER_TOP, TOP_ROUND = 104.5, 5.0              # measured
FINGER_STEPS = ((40.0, -15.3), (46.2, -13.8), (65.8, -12.0), (85.5, -10.0), (95.5, GRIP_FACE_X))   # the front: from z, at x  # measured
FINGER_WIDTH = ((44.0, 10.8), (105.0, 5.5))     # half its width (y) at the root and at the top  # measured

floor_top = GRIP_Z - SERVO.half_width      # the servo lies on the floor
servo_top = GRIP_Z + SERVO.half_width
case_y = (GRIP_Y - SERVO.case_half_height, GRIP_Y + SERVO.case_half_height)


def box(x, y, z):
    """A box spanning the (from, to) ranges x, y, z."""
    return (cq.Workplane("XY").box(x[1] - x[0], y[1] - y[0], z[1] - z[0])
            .translate(((x[0] + x[1]) / 2, (y[0] + y[1]) / 2, (z[0] + z[1]) / 2)))


def about_roll(z):
    """A plane across the roll axis at z, facing up."""
    return cq.Workplane("XY", origin=(ROLL_AXIS[0], ROLL_AXIS[1], z))


# the floor: narrow at the back block, wide under the servo, its front corners cut
half = [(BACK_X, BACK_HALF_WIDTH), (TAPER_FROM_X, BACK_HALF_WIDTH), (TAPER_TO_X, FLOOR_HALF_WIDTH),
        (FRONT_X - FRONT_CHAMFER, FLOOR_HALF_WIDTH), (FRONT_X, FLOOR_HALF_WIDTH - FRONT_CHAMFER)]
outline = half + [(x, -y) for x, y in reversed(half)]
jaw = (cq.Workplane("XY", origin=(0, 0, FLOOR_BOTTOM)).polyline(outline).close().extrude(floor_top - FLOOR_BOTTOM)
       .edges("|Z").fillet(CORNER_R))
# the boss on the roll horn, under the floor
tx, ty = BOSS_TAB
r_b = HORN_BOSS_D / 2
tab = [(tx, -ty), (tx, ty), (tx + 1.0, ty), (-r_b * 0.375, r_b * 0.92), (-r_b * 0.375, -r_b * 0.92), (tx + 1.0, -ty)]
jaw = jaw.union(about_roll(HORN_FACE_Z).circle(r_b).extrude(FLOOR_BOTTOM - HORN_FACE_Z)
                .union(about_roll(HORN_FACE_Z).polyline(tab).close().extrude(FLOOR_BOTTOM - HORN_FACE_Z)))
(cx0, cz0), (cx1, cz1) = TAB_CHAMFER
jaw = jaw.cut(cq.Workplane("XZ", origin=(0, HORN_BOSS_D, 0)).polyline([(cx0, cz0), (cx1, cz1), (cx1 - 5, cz1), (cx1 - 5, cz0 - 2), (cx0, cz0 - 2)])
              .close().extrude(2 * HORN_BOSS_D))

# the back block, and the finger rising from it
jaw = jaw.union(box((BACK_X, BLOCK_FRONT_X), (-BACK_HALF_WIDTH, BACK_HALF_WIDTH), (floor_top - 1, BLOCK_TOP)))
jaw = jaw.union(box((BACK_X, BLOCK_FRONT_X), (-ROOT_HALF_WIDTH, ROOT_HALF_WIDTH), (BLOCK_TOP, ROOT_TOP)))
# the finger: its side profile (x, z) through the full width, narrowed by its taper (y, z)
(bx0, bz0), (bx1, bz1) = FINGER_BACK
foot = ROOT_TOP - 6.0                      # sunk into the root slab
front = []                                 # down the stepped front, top to bottom
for i in range(len(FINGER_STEPS) - 1, -1, -1):
    z_from, x = FINGER_STEPS[i]
    z_to = FINGER_STEPS[i + 1][0] if i + 1 < len(FINGER_STEPS) else FINGER_TOP
    front += [(x, z_to), (x, z_from)]
profile = [(bx0, foot), (bx0, bz0), (bx1, bz1), (bx1 + TOP_ROUND, FINGER_TOP)] + front + [(FINGER_STEPS[0][1], foot)]
w = FINGER_WIDTH[0][1] + 1
finger = cq.Workplane("XZ", origin=(0, w, 0)).polyline(profile).close().extrude(2 * w)
(tz0, th0), (tz1, th1) = FINGER_WIDTH
taper = [(-th0, foot), (-th0, tz0), (-th1, tz1), (-th1, FINGER_TOP + 1), (th1, FINGER_TOP + 1), (th1, tz1), (th0, tz0), (th0, foot)]
finger = finger.intersect(cq.Workplane("YZ", origin=(bx0 - 1, 0, 0)).polyline(taper).close().extrude(GRIP_FACE_X - bx0 + 2))
jaw = jaw.union(finger)

# the side walls beside the servo's back, and the cap across them
for side in (1, -1):
    inner = case_y[1] if side > 0 else case_y[0]
    y = (inner, inner + side * WALL_THICKNESS)
    a, b, c = WALL_FRONT[side]             # its front edge leans back: a x + b z = c
    xs = [(c - b * z) / a for z in (floor_top - 1, servo_top)]
    wall = (cq.Workplane("XZ", origin=(0, max(y), 0))
            .polyline([(BLOCK_FRONT_X - 1, floor_top - 1), (xs[0], floor_top - 1), (xs[1], servo_top), (BLOCK_FRONT_X - 1, servo_top)])
            .close().extrude(max(y) - min(y)))
    jaw = jaw.union(wall)
# the back block widens with the floor's taper, up to the walls' tops
taper = [(TAPER_FROM_X, BACK_HALF_WIDTH), (TAPER_TO_X, FLOOR_HALF_WIDTH), (BLOCK_FRONT_X, FLOOR_HALF_WIDTH), (BLOCK_FRONT_X, BACK_HALF_WIDTH)]
for side in (1, -1):
    jaw = jaw.union(cq.Workplane("XY", origin=(0, 0, floor_top - 1)).polyline([(x, side * y) for x, y in taper]).close()
                    .extrude(servo_top - floor_top + 1))
# two nuts in the -y wall's inside, their screws out through it
n = NUT_POCKETS
inside = cq.Workplane(cq.Plane(origin=(0, case_y[0], 0), xDir=(1, 0, 0), normal=(0, -1, 0)))
pts = [(x, -n["z"]) for x in n["x"]]       # this plane's y is -z
jaw = jaw.cut(inside.pushPoints(pts).polygon(6, n["across_flats"] / math.cos(math.pi / 6)).extrude(n["depth"]))
jaw = jaw.cut(inside.pushPoints(pts).circle(n["hole_d"] / 2).extrude(WALL_THICKNESS + 1))
jaw = jaw.union(box((BLOCK_FRONT_X - 1, CAP_TO_X), (-CAP_HALF_WIDTH, CAP_HALF_WIDTH), (servo_top, servo_top + CAP_THICKNESS)))

# the gripper servo's pocket: its case, its raised faces recessed into the walls
jaw = jaw.cut(box((GRIP_X - SERVO.half_length, GRIP_X + SERVO.half_length + 1), case_y, (floor_top, servo_top)))
for f, inner in ((CASE_FACE_POS, case_y[1]), (CASE_FACE_NEG, case_y[0])):
    jaw = jaw.cut(box(f["x"], sorted((inner, f["y"])), f["z"]))

jaw = jaw.cut(about_roll(floor_top - SEAT_RECESS[1]).circle(SEAT_RECESS[0] / 2).extrude(SEAT_RECESS[1] + 1))

# the cable hole through the back block; five holes up the finger
jaw = jaw.cut(cq.Workplane("YZ", origin=(BACK_X - 1, 0, 0)).center(GRIP_Y, GRIP_Z).circle(CABLE_D / 2)
              .extrude(BLOCK_FRONT_X - BACK_X + 2))
(x0, z0), (dx, dz) = FINGER_HOLE_FROM, FINGER_HOLE_STEP
jaw = jaw.cut(cq.Workplane("XZ", origin=(0, ROOT_HALF_WIDTH + 1, 0))
              .pushPoints([(x0 + k * dx, z0 + k * dz) for k in range(5)]).circle(FINGER_HOLE_D / 2)
              .extrude(2 * ROOT_HALF_WIDTH + 2))

# -- interfaces, cut last -------------------------------------------------------------------------
# the roll horn's four screws down through the boss, their heads from above; the hub's access
horn = SERVO.horn.rotated(HORN_CLOCK_DEG)
jaw = jaw.cut(horn.on(about_roll(HORN_FACE_Z)).circle(HORN_SCREW_D / 2).extrude(floor_top))
jaw = jaw.cut(horn.on(about_roll(HORN_FACE_Z + HORN_SCREW_SEAT))
              .circle(HORN_SCREW_HEAD_D / 2).extrude(floor_top))
jaw = jaw.cut(about_roll(HORN_FACE_Z).circle(HUB_ACCESS_D / 2).extrude(floor_top))
# the gripper servo's screws through the walls, the heads from outside
for side in (1, -1):
    outer = (case_y[1] if side > 0 else case_y[0]) + side * WALL_THICKNESS
    wall = cq.Workplane(cq.Plane(origin=(SERVO_SCREW_X[side], outer, 0), xDir=(1, 0, 0), normal=(0, -side, 0)))
    pts = [(0, side * z) for z in SERVO_SCREW_Z]     # the plane's y is +z on the +y wall, -z on the other
    jaw = jaw.cut(wall.pushPoints(pts).circle(SERVO_SCREW.hole_d / 2).extrude(WALL_THICKNESS + 1))
    jaw = jaw.cut(wall.pushPoints(pts).circle(SERVO_SCREW.head_d / 2).extrude(WALL_THICKNESS - SERVO_SCREW.grip))

result = jaw
