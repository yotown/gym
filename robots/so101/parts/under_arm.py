"""SO-101 under arm (the forearm), written from its STEP: the interfaces exact, the body free.

Frame: the vendor's (Under_arm_SO101.step / Menagerie STL, mm): x along the arm from the wrist end
(x < 0, where the wrist-flex servo sits, sticking out past the end) to the elbow fork (x > 0); y
through the plate (y -44 .. -20, the top y = -20); z across the arm. The body is symmetric about
z = 0 except the elbow fork's -z tip, which is bevelled (the horn side), and the idler screw (+z).
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # SO-101's shared values (../shared.py): its servo, its screws
SERVO, SERVO_SCREW = S.SERVO, S.SERVO_SCREW

# -- interfaces: from the robot model (so101.xml) and the catalogue (feetech_sts3215) -- fixed ------
ELBOW_X, ELBOW_Y = 64.85, -32.0            # the elbow_flex axis, along z
SERVO_X, SERVO_Y, SERVO_Z = -57.55, -37.2, -0.5   # the wrist-flex STS3215's origin, its x reversed
# the case's raised faces inside the pocket, each a recess in a wall (the vendor's servo mesh)  # measured
CASE_STEP_NEG = dict(x=(-53.35, -40.1), y_top=-28.0, z=-18.2)    # on the -z side
CASE_STEP_POS = dict(x=(-53.85, -35.5), y_top=-30.2, z=16.5)     # on the +z side
HORN_SEAT_DEPTH = 1.5                      # the horn disc is d19.2; a seat in each tip's inner face
HORN_SCREW_D = 3.0
HORN_SCREW_WEB = 3.5                       # the screws' seat behind the horn face; heads from outside
HUB_DEPTH = 1.5                            # the horn's hub / the idler boss, below the seat
SERVO_SCREW_HEAD_SEAT_Z = 21.0             # their heads' seats, either side of the centre line
SERVO_SCREW_Y = -26.95
SERVO_SCREW_X = {1: -41.05, -1: -37.25}    # in the +z and the -z wall
FORK_GAP = 33.4                            # between the tips' inner faces: the elbow servo's horn and idler sit on them
THICKNESS = 24.0                           # the plate, centred on the elbow axis's height: the wrist holder against its top
WRIST_END_X, WRIST_HALF_WIDTH = -53.85, 23.0   # round the wrist motor holder
STEP_X = -25.85                            # the arm widens here, by the holder ...
EDGE_R = 5.0                               # every top and bottom edge (by the holder)
WRIST_CORNER_R = 3.0                       # by the holder

# -- body: free ------------------------------------------------------------------------------------
MID_HALF_WIDTH = 26.0                      # ... to this half width
TAPER_FROM_X, TAPER_TO_X = 14.15, 23.6     # ... and tapers out to the fork
FORK_HALF_WIDTH = 30.2
HUB_SLOT_WIDTH = 5.0                       # the hub's recess runs out to the top face
FORK_ROOT_X, FORK_ROOT_R = 23.0, 8.0       # the fork's gap: from this circle ...
FORK_JAW_X = 41.9                          # ... to the jaw
BEVEL_FROM_X, BEVEL_END_Z = 55.9, 20.7     # the horn tip's outer face, bevelled to the end  # measured
CABLE_LUG_X = (43.45, 53.95)               # two lugs on the horn tip's outside; a cable tie between
CABLE_LUG_Y, CABLE_LUG_HEIGHT = (-28.1, -36.05), 4.6
CABLE_LUG_PROUD, CABLE_LUG_R = 4.0, 0.8    # their outer corners rounded
SLOT_WIDTH, SLOT_END_X = 16.0, -10.85      # the slot behind the servo, its R8 round end here
ROOF_END_X, ROOF_UNDERSIDE_Y = -28.85, -24.8   # a roof over the servo, from the wrist end to here
VENT_SIDE = 3.4                            # square vents turned 45 deg (diamonds) through the roof
VENT_PITCH, VENT_GRID_AT = (10.0, 8.2), (-39.85, -0.5)

TIP_R = THICKNESS / 2                      # the fork tips, round about the axis in side view: tangent to both faces
TOP_Y = ELBOW_Y + THICKNESS / 2
tip_x = ELBOW_X + TIP_R
bottom_y = TOP_Y - THICKNESS


def top_down(y_top=TOP_Y):
    """A plan sketch (x, z) on the plane y = y_top, cut or extruded down."""
    return cq.Workplane("XZ", origin=(0, y_top, 0))


def slot(from_x):
    """The slot behind the servo, in plan: from from_x to its round end."""
    return (cq.Sketch().push([((from_x + SLOT_END_X) / 2, 0)]).rect(SLOT_END_X - from_x, SLOT_WIDTH)
            .push([(SLOT_END_X, 0)]).circle(SLOT_WIDTH / 2).clean())


def across(z, facing):
    """A plane across the arm at z, facing +z (1) or -z (-1), centred on the elbow axis."""
    return cq.Workplane(cq.Plane(origin=(ELBOW_X, ELBOW_Y, z), xDir=(1, 0, 0), normal=(0, 0, facing)))


# the plan: a stepped, tapered bar, symmetric about z = 0
half = [(WRIST_END_X, WRIST_HALF_WIDTH), (STEP_X, WRIST_HALF_WIDTH), (STEP_X, MID_HALF_WIDTH),
        (TAPER_FROM_X, MID_HALF_WIDTH), (TAPER_TO_X, FORK_HALF_WIDTH), (tip_x, FORK_HALF_WIDTH)]
outline = half + [(x, -z) for x, z in reversed(half)]
arm = top_down().polyline(outline).close().extrude(THICKNESS)
arm = arm.edges("|Y and <X").fillet(WRIST_CORNER_R)

# the fork's gap, and the slot behind the servo
end, g = tip_x + 5, FORK_GAP / 2
fork = (cq.Sketch().arc((FORK_ROOT_X, 0), FORK_ROOT_R, 0, 360)
        .segment((FORK_JAW_X, g), (end, g)).segment((FORK_JAW_X, -g), (end, -g)).hull())
arm = arm.cut(top_down().placeSketch(fork).extrude(THICKNESS))
arm = arm.cut(top_down().placeSketch(slot(ROOF_END_X)).extrude(THICKNESS))

# every top and bottom edge rounded, the fork's and the slot's inside included (before the pocket),
# but not the roof's end: the roof is thinner than the rounding
roof_end = cq.selectors.BoxSelector((ROOF_END_X - 1, TOP_Y - 1, -SLOT_WIDTH), (ROOF_END_X + 1, TOP_Y + 1, SLOT_WIDTH))
arm = arm.faces(">Y or <Y").edges(-roof_end).fillet(EDGE_R)

# the horn tip's bevel
bevel = [(BEVEL_FROM_X, -FORK_HALF_WIDTH), (tip_x, -BEVEL_END_Z), (tip_x, -FORK_HALF_WIDTH)]
arm = arm.cut(top_down().polyline(bevel).close().extrude(THICKNESS))

# the fork tips, round about the elbow axis in side view
side = (cq.Workplane("XY").center((WRIST_END_X + ELBOW_X) / 2, ELBOW_Y)
        .rect(ELBOW_X - WRIST_END_X, THICKNESS).extrude(FORK_HALF_WIDTH + 1, both=True)
        .union(cq.Workplane("XY").center(ELBOW_X, ELBOW_Y).circle(TIP_R).extrude(FORK_HALF_WIDTH + 1, both=True)))
arm = arm.intersect(side)

# the cable-tie lugs on the horn tip's outside
lugs = (cq.Workplane("XY", origin=(0, 0, -FORK_HALF_WIDTH - CABLE_LUG_PROUD))
        .pushPoints([(sum(CABLE_LUG_X) / 2, y) for y in CABLE_LUG_Y])
        .rect(CABLE_LUG_X[1] - CABLE_LUG_X[0], CABLE_LUG_HEIGHT).extrude(CABLE_LUG_PROUD)
        .edges("|Y and <Z").fillet(CABLE_LUG_R))
arm = arm.union(lugs)

# the wrist-flex servo: its case, from below up to the roof, walls either side of it; the slot
# runs on under the roof
servo = (cq.Workplane("XY").box(2 * SERVO.half_length, 2 * SERVO.half_width, 2 * SERVO.case_half_height)
         .translate((SERVO_X, SERVO_Y, SERVO_Z)))
arm = arm.cut(servo)
for step, wall_z in ((CASE_STEP_NEG, SERVO_Z - SERVO.case_half_height), (CASE_STEP_POS, SERVO_Z + SERVO.case_half_height)):
    (x0, x1), z0, z1 = step["x"], min(wall_z, step["z"]), max(wall_z, step["z"])
    arm = arm.cut(cq.Workplane("XY").box(x1 - x0, step["y_top"] - bottom_y, z1 - z0)
                  .translate(((x0 + x1) / 2, (step["y_top"] + bottom_y) / 2, (z0 + z1) / 2)))
under_roof = SERVO_X + SERVO.half_length
arm = arm.cut(top_down(ROOF_UNDERSIDE_Y).placeSketch(slot(under_roof)).extrude(ROOF_UNDERSIDE_Y - bottom_y))

# the roof's vents: a grid of diamonds
vents = cq.Sketch().push([VENT_GRID_AT]).rarray(*VENT_PITCH, 2, 4).rect(VENT_SIDE, VENT_SIDE, angle=45)
arm = arm.cut(top_down().placeSketch(vents).extrude(THICKNESS))

# -- interfaces, cut last -------------------------------------------------------------------------
gap = FORK_GAP / 2
seat, web = gap + HORN_SEAT_DEPTH, gap + HORN_SEAT_DEPTH + HORN_SCREW_WEB
for inward in (-1, 1):                     # each tip's inner face, and into the tip
    arm = arm.cut(across(inward * gap, inward).circle(S.HORN_SEAT_D / 2).extrude(HORN_SEAT_DEPTH))
    arm = arm.cut(across(inward * seat, inward).circle(SERVO.hub_d / 2).extrude(HUB_DEPTH))
    arm = arm.cut(across(inward * seat, inward).center(0, inward * (TOP_Y - ELBOW_Y) / 2)
                  .rect(HUB_SLOT_WIDTH, TOP_Y - ELBOW_Y).extrude(HUB_DEPTH))
    # the horn's four screws through the web, their heads from outside
    arm = arm.cut(SERVO.horn.on(across(inward * seat, inward))
                  .circle(HORN_SCREW_D / 2).extrude(HORN_SCREW_WEB))
    arm = arm.cut(SERVO.horn.on(across(inward * web, inward))
                  .circle(S.HORN_SCREW_HEAD_D / 2).extrude(FORK_HALF_WIDTH))
# the idler's screw, through the +z tip
arm = arm.cut(across(seat, 1).circle(S.IDLER_SCREW_D / 2).extrude(FORK_HALF_WIDTH))
# the servo's screws, one through each wall of its pocket, the heads from outside
for side_z in (-1, 1):
    wall = cq.Workplane(cq.Plane(origin=(SERVO_SCREW_X[side_z], SERVO_SCREW_Y, side_z * WRIST_HALF_WIDTH),
                                 xDir=(1, 0, 0), normal=(0, 0, -side_z)))
    arm = arm.cut(wall.circle(SERVO_SCREW.hole_d / 2).extrude(WRIST_HALF_WIDTH))
    heads = cq.Workplane(cq.Plane(origin=(SERVO_SCREW_X[side_z], SERVO_SCREW_Y, side_z * SERVO_SCREW_HEAD_SEAT_Z),
                                  xDir=(1, 0, 0), normal=(0, 0, side_z)))
    arm = arm.cut(heads.circle(SERVO_SCREW.head_d / 2).extrude(WRIST_HALF_WIDTH))

result = arm
