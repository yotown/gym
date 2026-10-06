"""SO-101 base, written from its STEP: the interfaces exact, the body free.

Frame: the vendor's (Base_SO101.step / Menagerie STL, mm): y up from the table (y = 0), the
shoulder_pan axis vertical at x = 0, z = PAN_Z; symmetric about x = 0. A foot of two hexagonal
wings, vented and clamped to the table, and a low tower that holds the pan servo's far end (its
near end, round the axis, is held by base_motor_holder). The shoulder bracket's lower arm swings
in the gap between the foot and the servo.
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # SO-101's shared values (../shared.py): its servo, its screws
SERVO, SERVO_SCREW = S.SERVO, S.SERVO_SCREW

# -- interfaces: from the robot model (so101.xml) and the catalogue (feetech_sts3215) -- fixed ------
PAN_Y, PAN_Z = 46.1, 32.7                  # the pan STS3215's origin (x = 0): its axis along y,
# what stands proud of the case inside the tower (the vendor's servo mesh)  # measured
UNDER_FACE = dict(half_width=9.2, z_from=15.0, bottom=28.2)
TOP_FACE = dict(half_width=7.0, z_from=10.0, top=63.3)
BOTTOM_SCREWS = dict(x=SERVO.tab_half_pitch, z=12.4)      # up through the floor into the servo's lower tabs
TOP_SCREWS = dict(x=10.5, z=15.9)          # down through the top plate into its upper tabs
CLAMP_D, CLAMP_HEAD_D = 5.0, 8.1           # four screws to the table,
CLAMP_HEAD_SEAT_Y = 15.2                   # their heads' seat above the table
INNER_PEAK = (9.2, 25.8)                   # where each wing's inner edge and its pillar's meet (x, z)  # measured
WING_INNER = [(10.5, 48.5), (10.5, 28.0), INNER_PEAK, (9.5, -16.0)]   # each wing's inner edge, by the holder's feet (x, z), x > 0  # measured
CLAMPS = [(31.75, -7.5), (27.78, 62.27)]   # (x, z), mirrored in x
TOWER_FRONT_Z = -16.0                      # the tower's front face
WALL_OUTER_X = 17.35
WALL_CORNER = 3.0                          # their front-bottom outer corner, cut clear of base_motor_holder
TOP_PLATE_TOP = 72.0
TOP_PLATE_FROM, TOP_PLATE_SIDE_TO_Z = 63.1, 14.15   # the plate over the servo's far end,
CABLE_D, CABLE_Z = 11.0, 0.4               # up through the tower
TOP_PLATE_SIDE_R = 3.0                     # the top plate's two side edges
WALL_SLOPE_TO = (12.84, 20.58)             # the walls' tops slant down outwards, from the top plate's side to here  # measured

# -- body: free ------------------------------------------------------------------------------------
TOWER_BACK_Z = 20.6                        # the walls' cut-outs and the under-face pocket run back to here
PILLAR_HALF_WIDTH, PILLAR_TOP, PILLAR_TO_Z = 22.35, 38.0, 7.0   # the pillars beside the servo: outer face, top, back
FOOT_TOP, RIB_HEIGHT = 17.5, 2.4           # the foot stands on ribs
RIB_WIDTH, RIB_PITCH, RIB_COUNT = 3.0, 7.94, 5     # under each wing, from its inner edge out
WING_OUTER = [(43.27, -16.0), (43.27, 0.0), (55.46, 21.8), (55.46, 29.8), (31.7, 71.0), (23.8, 71.0)]   # each wing's outer edge (x, z), x > 0  # measured
EDGE_NOTCH = [(9.2, 8.47), (13.07, 15.24), (9.2, 20.26)]   # a V in each inner edge, up to the floor  # measured
WING_CORNER_R = 2.5
WING_TOP_R = 3.0                           # the wings' top edges, all round but the inner one (it meets the tower)  # measured
BRIDGE_TOP, BRIDGE_TO_Z = 9.4, 8.47        # the wings are one piece below this
VENT_DIAGONALS = (5.0, 8.66)               # diamonds through the wings, on a lattice
VENT_AT, VENT_A, VENT_B = (26.28, 4.35), (4.5, 7.79), (-5.5, 9.53)
VENT_ROWS = {0: (0, 2), 1: (-1, 3), 2: (-1, 3), 3: (-1, 3), 4: (-1, 2)}   # per row i: first and last j
VENT_MARGIN = 2.0                          # a diamond at the wing's edge is clipped this far inside it
FLOOR_FROM = 28.2                          # under the servo's case
WINDOW_Y = (35.2, 57.3)                    # the front block is open between these
HOLDER_CLEAR_Z = 18.3                      # the walls stop here under base_motor_holder (along WINDOW_Y)  # measured
TOP_PLATE_END_R, TOP_PLATE_END_Z = 11.0, 19.5       # its back end round  # measured

case_y = (PAN_Y - SERVO.case_half_height, PAN_Y + SERVO.case_half_height)
servo_end_z = PAN_Z - SERVO.half_length    # the servo's far end, against the front block
hw = SERVO.half_width

# the tower's and the front's edge rounds, last  # measured
TOWER_CORNER_R = 3.0                       # the walls' front outer corners, beside their corner cut
FRONT_EDGE_R = 2.5                         # the front face's edges: the top plate's, the pillars' outer ones, the bridge's top


def box(x, y, z):
    """A box spanning the (from, to) ranges x, y, z."""
    return (cq.Workplane("XY").box(x[1] - x[0], y[1] - y[0], z[1] - z[0])
            .translate(((x[0] + x[1]) / 2, (y[0] + y[1]) / 2, (z[0] + z[1]) / 2)))


def mirrored(x, y, z):
    """A box and its mirror image across x = 0."""
    return box(x, y, z).union(box((-x[1], -x[0]), y, z))


def plan(y):
    """A plan sketch (x, z) on the plane y, extruded down."""
    return cq.Workplane("XZ", origin=(0, y, 0))


# the foot: two wings on ribs, joined by a bridge
foot = None
WING = WING_OUTER + WING_INNER
inner_x, wing_front_z = WING_INNER[-1]   # the wing's inner front corner
wing_back_z = max(z for _, z in WING)
for s in (1, -1):
    wing = [(s * x, z) for x, z in WING]
    w = (plan(FOOT_TOP).polyline(wing).close().extrude(FOOT_TOP - RIB_HEIGHT).edges("|Y").fillet(WING_CORNER_R)
         .faces(">Y").edges(cq.selectors.BoxSelector((-100, FOOT_TOP - 1, -100), (100, FOOT_TOP + 1, 100)))
         .filter(lambda e: abs(e.Center().x) > inner_x + 2.0).fillet(WING_TOP_R))
    ribs = (plan(RIB_HEIGHT).pushPoints([(s * (inner_x + RIB_PITCH * (k + 0.8)), 0) for k in range(RIB_COUNT)])
            .rect(RIB_WIDTH, 2 * wing_back_z).extrude(RIB_HEIGHT))
    w = w.union(ribs.intersect(plan(RIB_HEIGHT).polyline(wing).close().extrude(RIB_HEIGHT)))
    foot = w if foot is None else foot.union(w)
foot = foot.union(box((-inner_x, inner_x), (RIB_HEIGHT, BRIDGE_TOP), (wing_front_z, BRIDGE_TO_Z)))
# the vents: a lattice of diamonds, filling each wing to a margin from its edge (clipped there)
dx, dz = VENT_DIAGONALS
diamond = [(dx / 2, 0), (0, dz / 2), (-dx / 2, 0), (0, -dz / 2)]
for s in (1, -1):
    centres = [(s * (VENT_AT[0] + i * VENT_A[0] + j * VENT_B[0]), VENT_AT[1] + i * VENT_A[1] + j * VENT_B[1])
               for i, (j0, j1) in VENT_ROWS.items() for j in range(j0, j1 + 1)]
    lattice = None
    for cx, cz in centres:
        d = plan(FOOT_TOP + 1).center(cx, cz).polyline(diamond).close().extrude(FOOT_TOP + 2)
        lattice = d if lattice is None else lattice.union(d)
    inset = plan(FOOT_TOP + 1).polyline([(s * x, z) for x, z in WING]).close().offset2D(-VENT_MARGIN).extrude(FOOT_TOP + 2)
    foot = foot.cut(lattice.intersect(inset))

# the tower: pillars either side of the servo, its floor, walls, a front block with a window,
# and a top plate over the servo's far end
pillar = [(inner_x, TOWER_FRONT_Z), (PILLAR_HALF_WIDTH, TOWER_FRONT_Z), (PILLAR_HALF_WIDTH, PILLAR_TO_Z), INNER_PEAK]
base = foot
for s in (1, -1):
    base = base.union(plan(PILLAR_TOP).polyline([(s * x, z) for x, z in pillar]).close().extrude(PILLAR_TOP - FOOT_TOP + 1))
base = base.union(box((-inner_x, inner_x), (FLOOR_FROM, case_y[0]), (TOWER_FRONT_Z, UNDER_FACE["z_from"])))   # the pillars are its sides
wall = ([(hw, TOWER_FRONT_Z), (WALL_OUTER_X - WALL_CORNER, TOWER_FRONT_Z), (WALL_OUTER_X, TOWER_FRONT_Z + WALL_CORNER)]
        + [(WALL_OUTER_X, TOP_PLATE_SIDE_TO_Z), WALL_SLOPE_TO, (hw, WALL_SLOPE_TO[1])])
for s in (1, -1):
    base = base.union(plan(TOP_PLATE_TOP).polyline([(s * x, z) for x, z in wall]).close().extrude(TOP_PLATE_TOP - PILLAR_TOP))
base = base.union(box((-hw, hw), (case_y[0], TOP_PLATE_TOP), (TOWER_FRONT_Z, servo_end_z)))
base = base.cut(box((-hw, hw), WINDOW_Y, (TOWER_FRONT_Z - 1, servo_end_z)))
w = WALL_OUTER_X
plate = (cq.Sketch().arc((0, TOP_PLATE_END_Z), TOP_PLATE_END_R, 0, 360)
         .segment((WALL_CORNER - w, TOWER_FRONT_Z), (w - WALL_CORNER, TOWER_FRONT_Z))
         .segment((-w, TOWER_FRONT_Z + WALL_CORNER), (w, TOWER_FRONT_Z + WALL_CORNER))
         .segment((-w, TOP_PLATE_SIDE_TO_Z), (w, TOP_PLATE_SIDE_TO_Z)).hull())
base = base.union(plan(TOP_PLATE_TOP).placeSketch(plate).extrude(TOP_PLATE_TOP - TOP_PLATE_FROM))
base = base.cut(mirrored((hw, WALL_OUTER_X + 1), WINDOW_Y, (HOLDER_CLEAR_Z, TOWER_BACK_Z + 1)))

# the V-notches along the wings' inner edges, up through the pillars
for s in (1, -1):
    base = base.cut(plan(FLOOR_FROM).polyline([(s * x, z) for x, z in EDGE_NOTCH]).close().extrude(FLOOR_FROM))

# the servo's pocket: its case, and what stands proud of it
base = base.cut(box((-hw, hw), case_y, (servo_end_z, PAN_Z + SERVO.half_length)))
u, t = UNDER_FACE, TOP_FACE
base = base.cut(box((-u["half_width"], u["half_width"]), (u["bottom"], case_y[0] + 1), (u["z_from"], TOWER_BACK_Z + 1)))
base = base.cut(box((-t["half_width"], t["half_width"]), (case_y[1] - 1, t["top"]), (t["z_from"], TOP_PLATE_END_Z + TOP_PLATE_END_R)))
# the cable hole up through the tower
base = base.cut(cq.Workplane("XZ", origin=(0, TOP_PLATE_TOP + 1, 0)).center(0, CABLE_Z).circle(CABLE_D / 2)
                .extrude(TOP_PLATE_TOP + 1 - FLOOR_FROM))

# the edge rounds: each set named by where it is
def edges_where(shape, along, **at):
    """The straight edges of a shape along an axis ('x', 'y' or 'z') whose centre lies at the given
    coordinates, or within a given (from, to) range (x matched either side of x = 0: the part is mirrored)."""
    axis = cq.Vector(*[1.0 if c == along else 0.0 for c in "xyz"])
    hits = []
    for e in shape.Edges():
        if e.geomType() != "LINE" or abs(abs(e.tangentAt(0.5).dot(axis)) - 1) > 1e-6:
            continue
        c = e.Center()
        val = lambda k: abs(c.x) if k == "x" else getattr(c, k)
        if all((v[0] - 0.05 <= val(k) <= v[1] + 0.05) if isinstance(v, tuple) else abs(val(k) - v) < 0.05 for k, v in at.items()):
            hits.append(e)
    return hits


front = TOWER_FRONT_Z
for r, find in ((TOWER_CORNER_R, lambda s: edges_where(s, "y", x=WALL_OUTER_X - WALL_CORNER, y=(PILLAR_TOP, TOP_PLATE_TOP), z=front)),
                (TOP_PLATE_SIDE_R, lambda s: edges_where(s, "z", x=WALL_OUTER_X, y=TOP_PLATE_TOP)),
                (FRONT_EDGE_R, lambda s: edges_where(s, "x", y=TOP_PLATE_TOP, z=front) + edges_where(s, "y", x=PILLAR_HALF_WIDTH, z=front)
                 + edges_where(s, "x", y=BRIDGE_TOP, z=front))):
    solid = base.val()
    base = cq.Workplane().add(solid.fillet(r, find(solid)))

# -- interfaces, cut last -------------------------------------------------------------------------
# the servo's screws: up through the floor, down through the top plate (heads from outside)
b, tp = BOTTOM_SCREWS, TOP_SCREWS
base = base.cut(plan(case_y[0]).pushPoints([(-b["x"], b["z"]), (b["x"], b["z"])]).circle(SERVO_SCREW.hole_d / 2)
                .extrude(case_y[0] - FLOOR_FROM))
top = plan(TOP_PLATE_TOP).pushPoints([(-tp["x"], tp["z"]), (tp["x"], tp["z"])])
base = base.cut(top.circle(SERVO_SCREW.hole_d / 2).extrude(TOP_PLATE_TOP - case_y[1]))
base = base.cut(top.circle(SERVO_SCREW.head_d / 2).extrude(TOP_PLATE_TOP - case_y[1] - SERVO_SCREW.grip))
# the four clamp screws through the foot, their heads from above
clamps = [(s * x, z) for x, z in CLAMPS for s in (1, -1)]
base = base.cut(plan(FOOT_TOP).pushPoints(clamps).circle(CLAMP_D / 2).extrude(FOOT_TOP))
base = base.cut(plan(FOOT_TOP + 1).pushPoints(clamps).circle(CLAMP_HEAD_D / 2).extrude(FOOT_TOP + 1 - CLAMP_HEAD_SEAT_Y))

result = base
