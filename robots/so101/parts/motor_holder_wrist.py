"""SO-101 wrist motor holder, written from its STEP: the interfaces exact, the body free.

A square tube around the back end of the wrist_flex servo (STS3215): a bottom plate it stands on,
a top plate, and two side walls; two jaws in the bottom corners take the servo's screws.
motor_holder_base is this holder with its own servo height and boss, a chamfered seat and a cable clip.
Frame: the vendor's (Motor_holder_SO101_Wrist STEP / Menagerie STL, mm): x along the servo (the tube
spans x -53.85 .. -25.85, the servo reaches out towards -x), y up through the plates, z across
the walls (the servo's output axis). The profile is drawn in the y-z plane and extruded along x.
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # SO-101's shared values (../shared.py): its servo, its screws
SERVO, SERVO_SCREW = S.SERVO, S.SERVO_SCREW
HOLDER = globals().get("HOLDER", {})       # a sibling holder's own values (motor_holder_base)

# -- interfaces: the held servo (so101.xml pose, catalogue feetech_sts3215), the cradle round it -- fixed
SERVO_Y, SERVO_Z = -37.2, HOLDER.get("servo_z", -0.7)   # its origin (its centre); its x, y along -x, -y
BOSS_WIDTH = 18.4                                  # its end bosses, along y                # measured
SCREW_X_TOP, SCREW_X_BOTTOM = -41.05, -37.25       # at the +z and the -z end
FLOOR_Y, ROOF_Y = -52.6, -17.0                     # outside of the bottom and top plates: in the next link's cradle
HALF_SPAN = 26.2                                   # outside of the walls, +- z
WALL = 3.0                                         # plates and walls alike
INNER_R = 5.0
JAW_TOP_Y = -44.2                                  # the jaws in the bottom corners, up to here
JAW_Z = (15.4, 16.4)                               # their inner faces, at the +z and the -z end
JAW_THICKNESS = 2.2                                # under the screw heads
X_FROM, LENGTH = -53.85, 28.0                      # the tube along x: its ends against the next link (under_arm; rotation_pitch for the base's)

# -- body: free ------------------------------------------------------------------------------------
SERVO_X = -57.55                                   # its origin along x: the envelope runs out past the tube's end, so free here
OUTER_R = 8.0                                      # the tube's outer corners
SEAT_CHAMFER = HOLDER.get("seat_chamfer", 0.0)     # the -z bottom corner chamfered at 45 deg instead (0: rounded as the others)
BOSS_TO = HOLDER.get("boss_to", SERVO.axis_span[1])   # the end bosses' room along z, from the -z end to here
VENT_DIAGONAL = 4.8                        # diamonds through both plates
VENT_PITCH = (10.0, 8.2)
VENT_GRID_AT = (-39.85, -0.5)


def along_x(y, z, h, w, r=0.0):
    """A rounded rectangle in the y-z plane, centred (y, z), extruded over the tube's length."""
    body = cq.Workplane("YZ", origin=(X_FROM, 0, 0)).center(y, z).rect(h, w).extrude(LENGTH)
    return body.edges("|X").fillet(r) if r else body


# the tube: outer rounded rectangle (or with its -z bottom corner chamfered) less the inner one
tube = along_x((FLOOR_Y + ROOF_Y) / 2, 0, ROOF_Y - FLOOR_Y, 2 * HALF_SPAN)
if SEAT_CHAMFER:
    tube = tube.edges("|X and (not(<Y and <Z))").fillet(OUTER_R).edges("|X and (<Y and <Z)").chamfer(SEAT_CHAMFER)
else:
    tube = tube.edges("|X").fillet(OUTER_R)
tube = tube.cut(along_x((FLOOR_Y + ROOF_Y) / 2, 0, ROOF_Y - FLOOR_Y - 2 * WALL, 2 * (HALF_SPAN - WALL), INNER_R))

# the jaws in the bottom corners, from the floor up
floor_top = FLOOR_Y + WALL
for jaw_z, side in zip(JAW_Z, (1, -1)):
    w = HALF_SPAN - WALL - jaw_z                   # out to the wall
    tube = tube.union(along_x((floor_top + JAW_TOP_Y) / 2, side * (jaw_z + w / 2), JAW_TOP_Y - floor_top, w))

# the vents: a grid of diamonds through both plates
vents = (cq.Workplane("XZ", origin=(0, ROOF_Y, 0)).center(*VENT_GRID_AT).rarray(*VENT_PITCH, 2, 4)
         .polygon(4, VENT_DIAGONAL).extrude(ROOF_Y - FLOOR_Y))
tube = tube.cut(vents)

# -- interfaces, cut last --------------------------------------------------------------------------
def interfaces(tube):
    """The servo's envelope and its screws, cut last (motor_holder_base adds its clip before them)."""
    # the servo's envelope: its body, and its end bosses along z
    body = cq.Workplane("XY").box(SERVO.length, SERVO.width, 2 * SERVO.case_half_height).translate((SERVO_X, SERVO_Y, SERVO_Z))
    bosses = (cq.Workplane("XY").box(SERVO.length, BOSS_WIDTH, BOSS_TO - SERVO.axis_span[0])
              .translate((SERVO_X, SERVO_Y, SERVO_Z + (SERVO.axis_span[0] + BOSS_TO) / 2)))
    tube = tube.cut(body).cut(bosses)
    # the servo's screws: through each jaw, heads from outside; and access holes through the walls
    for x, jaw_z, side in ((SCREW_X_TOP, JAW_Z[0], 1), (SCREW_X_BOTTOM, JAW_Z[1], -1)):
        reach = HALF_SPAN - jaw_z
        jaw = cq.Workplane("XY", origin=(x, SERVO_Y - SERVO.tab_half_pitch, side * HALF_SPAN))
        tube = tube.cut(jaw.circle(SERVO_SCREW.hole_d / 2).extrude(-side * reach))
        tube = tube.cut(jaw.circle(SERVO_SCREW.head_d / 2).extrude(-side * (reach - JAW_THICKNESS)))
        wall = cq.Workplane("XY", origin=(x, SERVO_Y + SERVO.tab_half_pitch, side * HALF_SPAN))
        tube = tube.cut(wall.circle(SERVO_SCREW.head_d / 2).extrude(-side * WALL))
    return tube


blank = tube
result = interfaces(blank)
