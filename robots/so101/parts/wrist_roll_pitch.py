"""SO-101 wrist roll-pitch (the wrist yoke), written from its STEP: the interfaces exact, the body free.

Frame: the vendor's (Wrist_Roll_Pitch_SO101.step / Menagerie STL, mm): z along the wrist-roll axis,
up towards the wrist-flex axis (along x, at z = FLEX_Z); y across the roll servo. Two side plates
hold the roll servo between them, a roof caps them, and two round ears carry the flex joint: the
horn on the +x ear, the idler on the -x ear. Symmetric about y = 0.
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # SO-101's shared values (../shared.py): its servo, its screws
SERVO, SERVO_SCREW = S.SERVO, S.SERVO_SCREW

# -- interfaces: from the robot model (so101.xml) and the catalogue (feetech_sts3215) -- fixed ------
FLEX_Z = 28.0                              # the wrist_flex axis, along x
HORN_FACE_X = 18.3                         # the flex servo's horn face
HORN_SCREW_D = 3.2
HORN_SCREW_SEAT_X = 21.1                   # the heads' seats, either ear (|x|)
HUB_RECESS_D, HUB_RECESS_TO = 8.4, 20.1    # the horn's hub / the idler boss, into each ear
ROLL_Z = -14.4                             # the wrist-roll STS3215's origin (z): its length along x,
# what stands proud of the case at its ends (the vendor's servo mesh): a low face under the +x ear
# (its top cap stands in the roof's opening), and a ridge under the case  # measured
TOP_FACE = dict(x=(15.0, 30.4), half_width=9.7, top=3.8)
UNDER_RIDGE = dict(x=(8.4, 35.7), half_width=7.5, bottom=-31.9)
SERVO_SCREW_HEAD_SEAT = 2.5                # their heads' seat, below the servo's underside
SERVO_SCREW_X = 29.0                       # through the lip under the servo, either side
IDLER_EAR_ROOT_TOP = 18.2                  # the idler ear's root: thicker below the disc, up to here  # measured
OPENING_TIP_X = -4.1                       # the opening's tip  # measured
IDLER_EAR_INNER_X = -18.1                  # the -x ear stands clear of the flex servo's idler-end disc
LIP_FROM_X = 12.1                          # the lip under the servo, clear of the follower's sweep

# -- body: free ------------------------------------------------------------------------------------
ROLL_X = 12.5                              # its origin along x, its half length: its pocket is clear of the servo there, so free
IDLER_EAR_ROOT_X, IDLER_EAR_ROOT_R = -16.6, 6.6   # the idler ear's root, blended to the roof  # measured
OPENING_NECK, OPENING_HALF_WIDTH = 4.0, 11.0   # the opening: 45 deg flanks, a neck, a wide end  # measured
PLATE_THICKNESS = 2.6
PLATE_TOP, PLATE_BOTTOM = 3.4, -34.4
PLATE_TOP_FROM_X, PLATE_BOTTOM_FROM_X = -8.0, 19.2
PLATE_BELLY = (0.0, -29.3)                 # the plates' bottom edge curves from the nose through here  # measured
# two vents slanted through each plate: bars from a square end, clipped at x and at their rise
VENT_START, VENT_ANGLE, VENT_WIDTH = (15.44, -24.59), 42.0, 6.0   # the lower one's end, its slant  # measured
VENT_PITCH_Z, VENT_TO_X, VENT_RISE = 13.79, 27.2, 10.8           # measured
NOSE_X, NOSE_Z = -20.5, -16.3              # where the plates' slanted edges meet the -x ear
NOSE_TIP_X, NOSE_HALF_WIDTH = -22.8, 10.0  # ahead of the servo the plates are solid to a 45 deg V, this wide  # measured
ROOF_TOP = 4.9
ROOF_EAVES, ROOF_RIDGE = 4.5, 5.9          # between the ears the roof is a low gable  # measured
EAR_R, EAR_OUTER_X = 12.0, 27.1            # the ears: round about the flex axis, as wide, this far out
IDLER_EAR_CORNER_R, IDLER_EAR_HEEL_R = 5.0, 8.0   # its outer corners, its outer bottom edge  # measured
FOOT_R, FOOT_CENTRE_Z, FOOT_BLEND_R = 10.0, 3.9, 23.0   # the +x ear's foot: a round out to the servo's end, blended in  # measured
CABLE_HALF_WIDTH = 4.0                     # the cable's way through the roof: an opening, then a channel under the +x ear
CABLE_LUG = dict(x=(-9.3, -5.2), z=(-20.7, -10.2), proud=5.0)   # on the -y plate, for a cable tie

case_top, case_bottom = ROLL_Z + SERVO.case_half_height, ROLL_Z - SERVO.case_half_height
servo_x0, servo_x1 = ROLL_X - SERVO.half_length, ROLL_X + SERVO.half_length
outer_y = SERVO.half_width + PLATE_THICKNESS


def box(x, y, z):
    """A box spanning the (from, to) ranges x, y, z."""
    return (cq.Workplane("XY").box(x[1] - x[0], y[1] - y[0], z[1] - z[0])
            .translate(((x[0] + x[1]) / 2, (y[0] + y[1]) / 2, (z[0] + z[1]) / 2)))


def ear(x_inner, x_outer, bottom):
    """An ear: round about the flex axis, as wide as the plates at its foot (a yz sketch, along x)."""
    sk = cq.Sketch().arc((0, FLEX_Z), EAR_R, 0, 360).segment((-EAR_R, bottom), (EAR_R, bottom)).hull()
    lo, hi = sorted((x_inner, x_outer))
    return cq.Workplane("YZ", origin=(lo, 0, 0)).placeSketch(sk).extrude(hi - lo)


# the side plates, either side of the roll servo, the bottom edge curving up to the nose
def side(y_from, y_to):
    """The plates' outline (seen from the side) between two y."""
    return (cq.Workplane("XZ", origin=(0, y_to, 0)).moveTo(servo_x1, PLATE_TOP)
            .lineTo(servo_x1, PLATE_BOTTOM).lineTo(PLATE_BOTTOM_FROM_X, PLATE_BOTTOM).threePointArc(PLATE_BELLY, (NOSE_X, NOSE_Z))
            .lineTo(PLATE_TOP_FROM_X, PLATE_TOP).close().extrude(y_to - y_from))
yoke = side(SERVO.half_width, outer_y).union(side(-outer_y, -SERVO.half_width))
# the nose: solid across ahead of the servo, but for a V open towards it
t, h = NOSE_TIP_X, NOSE_HALF_WIDTH
v = [(t, 0), (t + h, h), (servo_x1, h), (servo_x1, -h), (t + h, -h)]
nose = side(-outer_y, outer_y).cut(cq.Workplane("XY", origin=(0, 0, PLATE_BOTTOM - 1)).polyline(v).close().extrude(PLATE_TOP - PLATE_BOTTOM + 2))
yoke = yoke.union(nose.intersect(box((NOSE_X - 1, servo_x0), (-outer_y, outer_y), (PLATE_BOTTOM, case_top))))

# the roof on the servo's case, between the plates' tops; the ears on it; the lip under the servo
yoke = yoke.union(box((-EAR_OUTER_X, servo_x1), (-SERVO.half_width, SERVO.half_width), (case_top, ROOF_TOP)))
gable = [(-SERVO.half_width, case_top), (SERVO.half_width, case_top), (SERVO.half_width, ROOF_EAVES), (0, ROOF_RIDGE),
         (-SERVO.half_width, ROOF_EAVES)]
yoke = yoke.union(cq.Workplane("YZ", origin=(IDLER_EAR_INNER_X, 0, 0)).polyline(gable).close().extrude(HORN_FACE_X - IDLER_EAR_INNER_X))
idler_ear = ear(IDLER_EAR_INNER_X, -EAR_OUTER_X, NOSE_Z).faces("<Z").edges("<X").fillet(IDLER_EAR_HEEL_R)
yoke = yoke.union(idler_ear.edges("|Z and <X").fillet(IDLER_EAR_CORNER_R))
x, r = IDLER_EAR_ROOT_X, IDLER_EAR_ROOT_R
root = (cq.Workplane("XZ", origin=(0, EAR_R, 0)).moveTo(IDLER_EAR_INNER_X, case_top).lineTo(x + r, case_top)
        .lineTo(x + r, ROOF_EAVES).radiusArc((x, ROOF_EAVES + r), r).lineTo(x, IDLER_EAR_ROOT_TOP)
        .lineTo(IDLER_EAR_INNER_X, IDLER_EAR_ROOT_TOP).close().extrude(2 * EAR_R))
yoke = yoke.union(root)
# the +x ear: its face straight down, a concave blend into a round foot out to the servo's end
foot_x = servo_x1 - FOOT_R
blend_x = EAR_OUTER_X + FOOT_BLEND_R
blend_z = FOOT_CENTRE_Z + math.sqrt((FOOT_R + FOOT_BLEND_R) ** 2 - (blend_x - foot_x) ** 2)
a = math.atan2(blend_z - FOOT_CENTRE_Z, blend_x - foot_x)          # the two arcs meet on their line of centres
meet = (foot_x + FOOT_R * math.cos(a), FOOT_CENTRE_Z + FOOT_R * math.sin(a))
on_foot = (foot_x + FOOT_R * math.cos(a / 2), FOOT_CENTRE_Z + FOOT_R * math.sin(a / 2))
b = (math.pi + a + math.pi) / 2
on_blend = (blend_x + FOOT_BLEND_R * math.cos(b), blend_z + FOOT_BLEND_R * math.sin(b))
horn_ear = (cq.Workplane("XZ", origin=(0, EAR_R, 0)).moveTo(HORN_FACE_X, case_top).lineTo(servo_x1, case_top)
            .lineTo(servo_x1, FOOT_CENTRE_Z).threePointArc(on_foot, meet).threePointArc(on_blend, (EAR_OUTER_X, blend_z))
            .lineTo(EAR_OUTER_X, FLEX_Z).lineTo(HORN_FACE_X, FLEX_Z).close().extrude(2 * EAR_R))
yoke = yoke.union(horn_ear).union(ear(HORN_FACE_X, EAR_OUTER_X, case_top))
yoke = yoke.union(box((LIP_FROM_X, servo_x1), (-outer_y, outer_y), (PLATE_BOTTOM, case_bottom)))
lug = CABLE_LUG
yoke = yoke.union(box(lug["x"], (-outer_y - lug["proud"], -outer_y), lug["z"]))

# the cable's way: an opening through the roof, then a channel under the +x ear
t, n, w, c = OPENING_TIP_X, OPENING_NECK, OPENING_HALF_WIDTH, CABLE_HALF_WIDTH
half = [(t, 0), (t + c, c), (t + c + n, c), (t + n + w, w), (HORN_FACE_X, w), (HORN_FACE_X, c), (servo_x1 + 1, c)]
opening = half + [(x, -y) for x, y in reversed(half[1:])]
yoke = yoke.cut(cq.Workplane("XY", origin=(0, 0, case_top - 1)).polyline(opening).close().extrude(ROOF_RIDGE - case_top + 2))
# the plates' vents
up, across = (math.cos(math.radians(VENT_ANGLE)), math.sin(math.radians(VENT_ANGLE))), (-math.sin(math.radians(VENT_ANGLE)), math.cos(math.radians(VENT_ANGLE)))
for i in range(2):
    x0, z0 = VENT_START[0], VENT_START[1] + i * VENT_PITCH_Z
    ends = [(x0 + k * across[0] * VENT_WIDTH / 2, z0 + k * across[1] * VENT_WIDTH / 2) for k in (1, -1)]
    bar = ends + [(x + 2 * VENT_RISE * up[0], z + 2 * VENT_RISE * up[1]) for x, z in reversed(ends)]
    vent = cq.Workplane("XZ", origin=(0, outer_y + 1, 0)).polyline(bar).close().extrude(2 * outer_y + 2)
    yoke = yoke.cut(vent.intersect(box((x0 - VENT_WIDTH, VENT_TO_X), (-outer_y - 1, outer_y + 1), (z0 - VENT_WIDTH, z0 + VENT_RISE))))

# the roll servo's pocket: its case, and what stands proud of it
yoke = yoke.cut(box((servo_x0, servo_x1 + 1), (-SERVO.half_width, SERVO.half_width), (case_bottom, case_top)))
f = TOP_FACE
yoke = yoke.cut(box(f["x"], (-f["half_width"], f["half_width"]), (case_top - 1, f["top"])))
r = UNDER_RIDGE
yoke = yoke.cut(box(r["x"], (-r["half_width"], r["half_width"]), (r["bottom"], case_bottom + 1)))

# -- interfaces, cut last -------------------------------------------------------------------------
# each ear: the hub's recess, the horn's four screws, their heads from outside (the ears are alike:
# the horn may go on either side)
for inner, outward in ((HORN_FACE_X, 1), (IDLER_EAR_INNER_X, -1)):
    face = cq.Workplane(cq.Plane(origin=(inner, 0, FLEX_Z), xDir=(0, 1, 0), normal=(outward, 0, 0)))
    yoke = yoke.cut(face.circle(HUB_RECESS_D / 2).extrude(HUB_RECESS_TO - outward * inner))
    yoke = yoke.cut(SERVO.horn.on(face).circle(HORN_SCREW_D / 2).extrude(EAR_OUTER_X))
    seat = cq.Workplane(cq.Plane(origin=(outward * HORN_SCREW_SEAT_X, 0, FLEX_Z), xDir=(0, -outward, 0), normal=(outward, 0, 0)))
    yoke = yoke.cut(SERVO.horn.on(seat).circle(S.HORN_SCREW_HEAD_D / 2)
                    .extrude(EAR_OUTER_X))         # the heads' room, from the seat out of the ear
# the roll servo's two screws up through the lip, their heads from below
under = cq.Workplane("XY", origin=(0, 0, PLATE_BOTTOM)).pushPoints([(SERVO_SCREW_X, s * SERVO.tab_half_pitch) for s in (-1, 1)])
yoke = yoke.cut(under.circle(SERVO_SCREW.hole_d / 2).extrude(case_bottom - PLATE_BOTTOM))
yoke = yoke.cut(under.circle(SERVO_SCREW.head_d / 2).extrude(case_bottom - SERVO_SCREW_HEAD_SEAT - PLATE_BOTTOM))

result = yoke
