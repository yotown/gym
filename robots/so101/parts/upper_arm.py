"""SO-101 upper arm, written from its STEP: the interfaces exact, the body free.

Frame: the vendor's (SO-ARM100 STEP / Menagerie STL): x along the arm from the elbow end (x < 0)
to the shoulder end (x > 0), y up through the plate, z across it. The body is symmetric about
z = 0; only the shoulder's horn (-z fork tip) and idler (+z tip) differ.
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # SO-101's shared values (../shared.py): its servo, its screws
SERVO, SERVO_SCREW = S.SERVO, S.SERVO_SCREW

# -- interfaces: from the robot model (so101.xml) and the catalogue (feetech_sts3215) -- fixed ------
SHOULDER_X, SHOULDER_Y = 65.085, 12.0      # the shoulder_lift axis, along z
ELBOW_SERVO_X, ELBOW_SERVO_Z = -47.485, -0.5
# the case's raised faces inside the channel, each a recess in a wall (the vendor's servo mesh)  # measured
CASE_STEP_NEG = dict(x=(-56.9, -37.9), y_from=9.8, z=-19.9)       # on the -z side
CASE_STEP_POS = dict(x=(-54.48, -40.48), y_from=4.8, z=16.5)      # on the +z side
HORN_SEAT_DEPTH = 1.5                      # the horn disc is d19.2
HORN_SCREW_D = 3.0
HORN_SCREW_HEAD_SEAT = 12.0                # the heads' seat, out from the -z tip's inner face
CENTRE_BORE_DEPTH = 1.5                    # the horn's hub / the idler boss
SERVO_SCREW_Y = {-1: 7.2, 1: 11.0}         # their height, in the -z wall and in the +z wall (the servo's ears are offset)
SERVO_SCREW_HEAD_SEAT_Z = 23.0             # their heads' seats, either side of the centre line
FORK_GAP = 33.4                            # between the tips' inner faces: the shoulder servo's horn and idler sit on them
FLOOR = 4.8                                # the channel's floor: the elbow servo stands on it (y)

# -- body: free ------------------------------------------------------------------------------------
FORK_JAW_X = 41.08                         # the fork's straight jaw, from here to the end
THICKNESS = 24.0                           # the plate, centred on the shoulder axis's height
ELBOW_END_X = -65.085
ELBOW_HALF_WIDTH, SHOULDER_HALF_WIDTH = 25.0, 31.7
TAPER_FROM_X, TAPER_TO_X = -19.46, 8.66
EDGE_R = 5.0                               # the long top and bottom edges
ELBOW_CORNER_R = 2.0
FORK_ROOT_X, FORK_ROOT_R = 23.0, 8.0       # the fork's gap: from this circle to the jaw
CABLE_WIDTH, CABLE_END_X = 16.0, -19.08    # the centre channel, its R8 round end here
CABLE_HOLE_FROM_X = -29.1                  # through the floor from here (the D hole)
VENT_DIAGONAL = 4.8
VENT_PITCH = (7.7, 8.2)
VENT_GRID_AT = (-46.63, -0.5)
CABLE_LUG_X = (38.63, 49.14)               # two lugs on the -z side's outside; a cable tie between  # measured
CABLE_LUG_Y = ((5.31, 10.81), (13.59, 18.38))                                                     # measured
CABLE_LUG_PROUD, CABLE_LUG_R = 3.9, 0.8    # their outer corners rounded

TIP_R = THICKNESS / 2                      # the shoulder end, round about the axis in side view: tangent to both faces
bottom, top = SHOULDER_Y - THICKNESS / 2, SHOULDER_Y + THICKNESS / 2
tip_x = SHOULDER_X + TIP_R


def top_down(depth, y_top=None):
    """A plan sketch (x, z) on the plane y = y_top, cut or extruded `depth` down."""
    return cq.Workplane("XZ", origin=(0, top if y_top is None else y_top, 0))


# the plan: a tapered bar, symmetric about z = 0
half = [(ELBOW_END_X, ELBOW_HALF_WIDTH), (TAPER_FROM_X, ELBOW_HALF_WIDTH),
        (TAPER_TO_X, SHOULDER_HALF_WIDTH), (tip_x, SHOULDER_HALF_WIDTH)]
outline = half + [(x, -z) for x, z in reversed(half)]
arm = top_down(THICKNESS).polyline(outline).close().extrude(THICKNESS)
arm = arm.edges("|Y and <X").fillet(ELBOW_CORNER_R)

# the shoulder end, round about the axis in side view
side = (cq.Workplane("XY").center((ELBOW_END_X + SHOULDER_X) / 2, SHOULDER_Y)
        .rect(SHOULDER_X - ELBOW_END_X, THICKNESS).extrude(SHOULDER_HALF_WIDTH + 1, both=True)
        .union(cq.Workplane("XY").center(SHOULDER_X, SHOULDER_Y).circle(TIP_R).extrude(SHOULDER_HALF_WIDTH + 1, both=True)))
arm = arm.intersect(side)

# the fork: the gap between the tips
end, g = tip_x + 5, FORK_GAP / 2
fork = (cq.Sketch().arc((FORK_ROOT_X, 0), FORK_ROOT_R, 0, 360)
        .segment((FORK_JAW_X, g), (end, g)).segment((FORK_JAW_X, -g), (end, -g)).hull())
arm = arm.cut(top_down(THICKNESS).placeSketch(fork).extrude(THICKNESS))

# the plate's top and bottom edges rounded, the fork's inside included (before any pocket is cut)
arm = arm.faces(">Y or <Y").edges().fillet(EDGE_R)

# the cable-tie lugs on the -z side
for y0, y1 in CABLE_LUG_Y:
    arm = arm.union(cq.Workplane("XY", origin=(0, 0, -SHOULDER_HALF_WIDTH - CABLE_LUG_PROUD))
                    .center(sum(CABLE_LUG_X) / 2, (y0 + y1) / 2)
                    .rect(CABLE_LUG_X[1] - CABLE_LUG_X[0], y1 - y0).extrude(CABLE_LUG_PROUD)
                    .edges("|Y and <Z").fillet(CABLE_LUG_R))

# the elbow servo's channel: its case, from the top down to the floor it stands on, walls either side
arm = arm.cut(top_down(top - FLOOR).center(ELBOW_SERVO_X, ELBOW_SERVO_Z)
              .rect(SERVO.width, 2 * SERVO.case_half_height).extrude(top - FLOOR))
for step, wall_z in ((CASE_STEP_NEG, ELBOW_SERVO_Z - SERVO.case_half_height), (CASE_STEP_POS, ELBOW_SERVO_Z + SERVO.case_half_height)):
    (x0, x1), z0, z1 = step["x"], min(wall_z, step["z"]), max(wall_z, step["z"])
    arm = arm.cut(cq.Workplane("XY").box(x1 - x0, top - step["y_from"], z1 - z0)
                  .translate(((x0 + x1) / 2, (top + step["y_from"]) / 2, (z0 + z1) / 2)))
# the cable channel along the centre line, down to the floor
cable = (cq.Sketch().push([((ELBOW_END_X - 5 + CABLE_END_X) / 2, 0)]).rect(CABLE_END_X - ELBOW_END_X + 5, CABLE_WIDTH)
         .push([(CABLE_END_X, 0)]).circle(CABLE_WIDTH / 2).clean())
arm = arm.cut(top_down(top - FLOOR).placeSketch(cable).extrude(top - FLOOR))
hole = (cq.Sketch().push([((CABLE_HOLE_FROM_X + CABLE_END_X) / 2, 0)]).rect(CABLE_END_X - CABLE_HOLE_FROM_X, CABLE_WIDTH)
        .push([(CABLE_END_X, 0)]).circle(CABLE_WIDTH / 2).clean())
arm = arm.cut(top_down(FLOOR - bottom, FLOOR).placeSketch(hole).extrude(FLOOR - bottom))

# the floor's vents: a grid of diamonds under the servo
vents = (top_down(FLOOR - bottom, FLOOR).center(*VENT_GRID_AT).rarray(*VENT_PITCH, 4, 4)
         .polygon(4, VENT_DIAGONAL).extrude(FLOOR - bottom))
arm = arm.cut(vents)

# -- interfaces, cut last -------------------------------------------------------------------------
gap = FORK_GAP / 2
for side_z, inward in ((-gap, -1), (gap, 1)):     # each tip's inner face, and into the tip
    face = cq.Plane(origin=(SHOULDER_X, SHOULDER_Y, side_z), xDir=(1, 0, 0), normal=(0, 0, inward))
    arm = arm.cut(cq.Workplane(face).circle(S.HORN_SEAT_D / 2).extrude(HORN_SEAT_DEPTH))
    arm = arm.cut(cq.Workplane(face).circle(SERVO.hub_d / 2).extrude(HORN_SEAT_DEPTH + CENTRE_BORE_DEPTH))
# the horn's screws, through the -z tip, their heads from outside
horn = cq.Plane(origin=(SHOULDER_X, SHOULDER_Y, -gap), xDir=(1, 0, 0), normal=(0, 0, -1))
arm = arm.cut(SERVO.horn.on(cq.Workplane(horn))
              .circle(HORN_SCREW_D / 2).extrude(SHOULDER_HALF_WIDTH))
seat = cq.Plane(origin=(SHOULDER_X, SHOULDER_Y, -gap - HORN_SCREW_HEAD_SEAT), xDir=(1, 0, 0), normal=(0, 0, -1))
arm = arm.cut(SERVO.horn.on(cq.Workplane(seat))
              .circle(S.HORN_SCREW_HEAD_D / 2).extrude(SHOULDER_HALF_WIDTH))
# the idler's screw, through the +z tip
arm = arm.cut(cq.Workplane(cq.Plane(origin=(SHOULDER_X, SHOULDER_Y, gap), xDir=(1, 0, 0), normal=(0, 0, 1)))
              .circle(S.IDLER_SCREW_D / 2).extrude(SHOULDER_HALF_WIDTH))
# the elbow servo's screws, through both walls of its channel
for z_side in (-1, 1):
    pts = [(dx_, SERVO_SCREW_Y[z_side]) for dx_ in (-SERVO.tab_half_pitch, SERVO.tab_half_pitch)]
    holes = cq.Plane(origin=(ELBOW_SERVO_X, 0, 0), xDir=(1, 0, 0), normal=(0, 0, z_side))   # its y is the world's y
    arm = arm.cut(cq.Workplane(holes).pushPoints(pts).circle(SERVO_SCREW.hole_d / 2).extrude(ELBOW_HALF_WIDTH + 1))
    heads = cq.Plane(origin=(ELBOW_SERVO_X, 0, z_side * SERVO_SCREW_HEAD_SEAT_Z), xDir=(1, 0, 0), normal=(0, 0, z_side))
    arm = arm.cut(cq.Workplane(heads).pushPoints([(x, y) for x, y in pts]).circle(SERVO_SCREW.head_d / 2).extrude(ELBOW_HALF_WIDTH))

result = arm
