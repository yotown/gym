"""SO-101 rotation pitch (the shoulder bracket), written from its STEP: the interfaces exact, the body free.

Frame: the vendor's (Rotation_Pitch_SO101.step / Menagerie STL, mm): y up along the shoulder_pan
axis, x from the column at the back (x < 0) towards the pan axis, z across. A C-shaped bracket: the
lower arm rests on the pan servo's horn, the upper arm over its idler, a column joins them at the
back, and a cradle on top holds the shoulder_lift servo.
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # SO-101's shared values (../shared.py): its servo, its screws
SERVO, SERVO_SCREW = S.SERVO, S.SERVO_SCREW

# -- interfaces: from the robot model (so101.xml) and the catalogue (feetech_sts3215) -- fixed ------
PAN_X, PAN_Z = -12.201, -0.022             # the shoulder_pan axis, along y
HORN_FACE_Y = 10.0                         # the pan servo's horn face: the lower arm's top
IDLER_FACE_Y = 47.9                        # its idler boss's end, inside the upper arm
HORN_SCREW_D = 3.2
HORN_SCREW_SEAT = 3.5                      # the screws' seat under the horn; heads from below
HUB_SLOT_WIDTH = 6.2                       # the horn's centre screw, run out to the arm's end; not in the model: that screw's head
HUB_SLOT_DEPTH = 1.0
IDLER_CLEARANCE = 0.5                      # the idler boss, with room past its end
LIFT_X, LIFT_Y, LIFT_Z = -42.6, 88.1, 0.4  # the shoulder_lift STS3215's origin: its length along y,
# the case's raised faces, each a recess in a side wall (the vendor's servo mesh)  # measured
CASE_STEP_POS = dict(x_from=-51.8, z=18.2, y_from=70.4)  # the +z side, from x_from to the front, above y_from
CASE_STEP_NEG = dict(x_from=-49.6, z=-16.7, y_from=65.4)  # the -z side, from the floor
SERVO_SCREWS = [(-52.85, 67.8, 1), (-52.85, 71.6, -1)]    # (x, y, side): one through each wall
UPPER_ARM_FROM, UPPER_ARM_TO = 46.4, 56.4    # the upper arm, round the pan servo's idler; the shoulder holder above it
BACK_X = -59.8
SKIRT_CLEAR_R = 10.1                       # under the upper arm, clear of the idler  # measured
CRADLE_HALF_WIDTH, CRADLE_CORNER_R, CRADLE_FOOT_R = 23.0, 5.0, 8.0   # the cradle round the shoulder motor holder
FLOOR_FRONT_X, WALL_FRONT_X = -30.3, -35.8
ACCESSORY_D, ACCESSORY_PITCH, ACCESSORY_AT_Y = 1.5, 25.4, 33.95   # accessories' screws, on a 1 in square
ACCESSORY_DEPTH = 6.0                      # not in the model: the accessories' screws

# -- body: free ------------------------------------------------------------------------------------
COLUMN_HALF_WIDTH, COLUMN_BACK_DEPTH = 19.7, 6.5   # the column at the back
SKIRT_FRONT_X = -18.3                      # the skirt under the upper arm, its outline again, forward to here  # measured
CRADLE_TOP = 84.4                          # the cradle's walls, up to here
TOOL_ACCESS_D = 5.4                        # over the horn screws, through the upper arm
BOTTOM_Y = 0.2                             # measured
COLUMN_APEX_X = -35.0                      # the column tapers to an edge towards the pan servo
ARM_END_R = 12.0                           # the arms end round about the pan axis
WAIST_X, WAIST_HALF_WIDTH = -28.24, 10.04  # the arms narrow from the column's corners to a waist  # measured
WAIST_R = 4.2
ROOT_FRONT_X, ROOT_FRONT_HALF_WIDTH = -33.0, 4.0   # where an arm meets the column it is thicker: a root
ROOT_SHOULDER_X = -42.5                    # the root's corners cut from here on the arm's flank  # measured
ROOT_DEPTH = (4.8, 3.8)                    # the lower arm's root, the upper arm's  # measured
WEB_SHOULDER_X, WEB_APEX_X, WEB_APEX_R = -38.8, -23.0, 2.0   # on the lower arm a thin web from the root to a point  # measured
WEB_DEPTH = 1.4                            # measured
BOTTOM_CHAMFER = 12.4                      # the back's bottom edge, 45 deg  # measured
CORNER_R = 3.0
SIDE_WALL_DROP, SIDE_WALL_STEP = 2.0, 1.6   # the +z wall is lower than the back wall, stepped down from it  # measured
HOLDER_NOTCH_HALF_WIDTH = 13.0          # the floor's front is this narrow: the lift servo's holder sits either side
VENT_DIAGONAL, VENT_PITCH_Y, VENT_PITCH_Z, VENT_AT_Y = 4.8, 10.0, 8.2, 70.4   # a 2 x 4 grid of diamonds in the back wall

floor_top = LIFT_Y - SERVO.half_length     # the lift servo stands on the floor
servo_back_x = LIFT_X - SERVO.half_width


def plan(y_top):
    """A plan sketch (x, z) on the plane y = y_top, extruded or cut down."""
    return cq.Workplane("XZ", origin=(0, y_top, 0))


def about_pan(y):
    """A plane across the pan axis at y, facing up."""
    return cq.Workplane(cq.Plane(origin=(PAN_X, y, PAN_Z), xDir=(1, 0, 0), normal=(0, 1, 0)))


# the column: a back wall tapering to an edge towards the pan servo
hw = COLUMN_HALF_WIDTH
column = (plan(UPPER_ARM_TO).polyline([(BACK_X, -hw), (BACK_X + COLUMN_BACK_DEPTH, -hw), (COLUMN_APEX_X, 0),
                                        (BACK_X + COLUMN_BACK_DEPTH, hw), (BACK_X, hw)]).close()
          .extrude(UPPER_ARM_TO - BOTTOM_Y).edges("|Y").fillet(CORNER_R))

# the arms: from the column's corners in to a waist, then out along a tangent to a round end about the pan axis
corner_x = BACK_X + COLUMN_BACK_DEPTH
def tangent_from(z_waist, side):
    """Where the line from the waist corner (WAIST_X, z_waist) touches the end circle about the pan axis."""
    dx, dz = WAIST_X - PAN_X, z_waist - PAN_Z
    t = math.atan2(dz, dx) - side * math.acos(ARM_END_R / math.hypot(dx, dz))
    return (PAN_X + ARM_END_R * math.cos(t), PAN_Z + ARM_END_R * math.sin(t))


tangent, tangent_low = tangent_from(WAIST_HALF_WIDTH, 1), tangent_from(-WAIST_HALF_WIDTH, -1)
half = [(BACK_X, hw), (corner_x, hw), (WAIST_X, WAIST_HALF_WIDTH), tangent]
def arm(y_from, y_to):
    """The arm's outline between two levels, its waist rounded."""
    body = (plan(y_to).polyline(half).threePointArc((PAN_X + ARM_END_R, PAN_Z), tangent_low)
            .polyline([(x, -z) for x, z in reversed(half[:-1])], includeCurrent=True).close().extrude(y_to - y_from))
    for side in (1, -1):
        waist = cq.selectors.NearestToPointSelector((WAIST_X, (y_from + y_to) / 2, side * WAIST_HALF_WIDTH))
        body = body.edges(waist).fillet(WAIST_R)
    return body
def layer(outline, y_from, y_to):
    return plan(y_to).polyline(outline).close().extrude(y_to - y_from)
# an arm's root: the arm's outline stopped short of the waist, its corners cut
flank = lambda x: hw + (x - corner_x) * (WAIST_HALF_WIDTH - hw) / (WAIST_X - corner_x)
root = [(BACK_X, hw), (corner_x, hw), (ROOT_SHOULDER_X, flank(ROOT_SHOULDER_X)), (ROOT_FRONT_X, ROOT_FRONT_HALF_WIDTH)]
root = root + [(x, -z) for x, z in reversed(root)]
web = [(BACK_X, hw), (corner_x, hw), (WEB_SHOULDER_X, flank(WEB_SHOULDER_X)), (WEB_APEX_X, 0),
       (WEB_SHOULDER_X, -flank(WEB_SHOULDER_X)), (corner_x, -hw), (BACK_X, -hw)]
web = layer(web, HORN_FACE_Y, HORN_FACE_Y + WEB_DEPTH)
web = web.edges(cq.selectors.NearestToPointSelector((WEB_APEX_X, HORN_FACE_Y, 0))).fillet(WEB_APEX_R)
lower = arm(BOTTOM_Y, HORN_FACE_Y).union(layer(root, HORN_FACE_Y, HORN_FACE_Y + ROOT_DEPTH[0])).union(web)
skirt = (arm(UPPER_ARM_FROM - WEB_DEPTH, UPPER_ARM_FROM)
         .cut(plan(UPPER_ARM_FROM).center(SKIRT_FRONT_X + ARM_END_R, 0).rect(2 * ARM_END_R, 2 * hw).extrude(WEB_DEPTH))
         .cut(plan(UPPER_ARM_FROM).center(PAN_X, PAN_Z).circle(SKIRT_CLEAR_R).extrude(WEB_DEPTH)))
upper = (arm(UPPER_ARM_FROM, UPPER_ARM_TO).union(layer(root, UPPER_ARM_FROM - ROOT_DEPTH[1], UPPER_ARM_FROM))
         .union(skirt))
bracket = column.union(lower).union(upper)
# the back's bottom edge chamfered
bracket = bracket.cut(cq.Workplane("XY", origin=(0, 0, -hw - 1)).polyline(
    [(BACK_X - 1, BOTTOM_Y - 1), (BACK_X + BOTTOM_CHAMFER + 1, BOTTOM_Y - 1), (BACK_X - 1, BOTTOM_Y + BOTTOM_CHAMFER + 1)])
    .close().extrude(2 * hw + 2))

# the cradle for the lift servo, on top of the column
cradle = (cq.Workplane("XY").box(FLOOR_FRONT_X - BACK_X, CRADLE_TOP - UPPER_ARM_TO, 2 * CRADLE_HALF_WIDTH)
          .translate(((BACK_X + FLOOR_FRONT_X) / 2, (UPPER_ARM_TO + CRADLE_TOP) / 2, 0))
          .edges("|Y").fillet(CRADLE_CORNER_R).faces("<Y").edges("|X").fillet(CRADLE_FOOT_R))
# the side walls stop short of the floor's front
cradle = cradle.cut(cq.Workplane("XY").box(FLOOR_FRONT_X - WALL_FRONT_X + 1, CRADLE_TOP - floor_top, 2 * CRADLE_HALF_WIDTH + 2)
                    .translate(((WALL_FRONT_X + FLOOR_FRONT_X + 1) / 2, (floor_top + CRADLE_TOP) / 2, 0)))
part = bracket.union(cradle)
for s in (1, -1):
    z = sorted((s * HOLDER_NOTCH_HALF_WIDTH, s * (CRADLE_HALF_WIDTH + 1)))
    part = part.cut(cq.Workplane("XY").box(FLOOR_FRONT_X + 1 - WALL_FRONT_X, floor_top - UPPER_ARM_TO, z[1] - z[0])
                    .translate(((WALL_FRONT_X + FLOOR_FRONT_X + 1) / 2, (UPPER_ARM_TO + floor_top) / 2, sum(z) / 2)))

# the lift servo's pocket: its case, walls either side, the case's raised faces recessed
z0, z1 = LIFT_Z - SERVO.case_half_height, LIFT_Z + SERVO.case_half_height
front = LIFT_X + SERVO.half_width + 1
for x_from, y_from, za, zb in ((servo_back_x, floor_top, z0, z1),
                               (CASE_STEP_POS["x_from"], CASE_STEP_POS["y_from"], z1, CASE_STEP_POS["z"]),
                               (CASE_STEP_NEG["x_from"], CASE_STEP_NEG["y_from"], CASE_STEP_NEG["z"], z0)):
    part = part.cut(cq.Workplane("XY").box(front - x_from, CRADLE_TOP + 1 - y_from, zb - za)
                    .translate(((x_from + front) / 2, (y_from + CRADLE_TOP + 1) / 2, (za + zb) / 2)))

# vents through the back wall, behind the lift servo
vents = (cq.Workplane("YZ", origin=(BACK_X - 1, 0, 0)).center(VENT_AT_Y, LIFT_Z)
         .rarray(VENT_PITCH_Y, VENT_PITCH_Z, 2, 4).polygon(4, VENT_DIAGONAL).extrude(FLOOR_FRONT_X - BACK_X + 2))   # cut through all
part = part.cut(vents)
# the +z wall's top lowered, stepping down from the back wall
top = CRADLE_TOP - SIDE_WALL_DROP
part = part.cut(cq.Workplane("XY", origin=(0, 0, z1)).polyline(
    [(servo_back_x, CRADLE_TOP + 1), (servo_back_x, CRADLE_TOP), (servo_back_x + SIDE_WALL_STEP, top),
     (FLOOR_FRONT_X, top), (FLOOR_FRONT_X, CRADLE_TOP + 1)]).close().extrude(CRADLE_HALF_WIDTH + 1 - z1))
# four small holes in the column's back, for an accessory
part = part.cut(cq.Workplane("YZ", origin=(BACK_X, 0, 0)).center(ACCESSORY_AT_Y, 0)
                .rarray(ACCESSORY_PITCH, ACCESSORY_PITCH, 2, 2).circle(ACCESSORY_D / 2).extrude(ACCESSORY_DEPTH))

# -- interfaces, cut last -------------------------------------------------------------------------
# the horn's screws up through the lower arm, their heads from below; the hub's slot on top
part = part.cut(SERVO.horn.on(about_pan(BOTTOM_Y)).circle(HORN_SCREW_D / 2)
                .extrude(HORN_FACE_Y - BOTTOM_Y))
part = part.cut(SERVO.horn.on(about_pan(BOTTOM_Y)).circle(S.HORN_SCREW_HEAD_D / 2)
                .extrude(HORN_FACE_Y - HORN_SCREW_SEAT - BOTTOM_Y))
part = part.cut(about_pan(HORN_FACE_Y - HUB_SLOT_DEPTH).center(ARM_END_R / 2, 0)
                .rect(ARM_END_R + 1, HUB_SLOT_WIDTH).extrude(HUB_SLOT_DEPTH))
# the idler boss's recess under the upper arm, its screw through; tool access over the horn screws
recess_to = IDLER_FACE_Y + IDLER_CLEARANCE
part = part.cut(about_pan(UPPER_ARM_FROM).circle(SERVO.hub_d / 2).extrude(recess_to - UPPER_ARM_FROM))
part = part.cut(about_pan(UPPER_ARM_FROM).circle(S.IDLER_SCREW_D / 2).extrude(UPPER_ARM_TO - UPPER_ARM_FROM))
part = part.cut(SERVO.horn.on(about_pan(UPPER_ARM_FROM)).circle(TOOL_ACCESS_D / 2)
                .extrude(UPPER_ARM_TO - UPPER_ARM_FROM))
# the lift servo's screws, one through each wall, the heads from outside
for x, y, side in SERVO_SCREWS:
    inner = z1 if side > 0 else z0
    wall = cq.Workplane(cq.Plane(origin=(x, y, side * CRADLE_HALF_WIDTH), xDir=(1, 0, 0), normal=(0, 0, -side)))
    part = part.cut(wall.circle(SERVO_SCREW.hole_d / 2).extrude(CRADLE_HALF_WIDTH))
    part = part.cut(wall.circle(SERVO_SCREW.head_d / 2).extrude(CRADLE_HALF_WIDTH - side * inner - SERVO_SCREW.grip))

result = part
