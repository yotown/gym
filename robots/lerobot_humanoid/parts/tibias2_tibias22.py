"""LeRobot humanoid tibia (tibias 22), written from its STEP: a back plate, a front plate that carries
the knee actuator, an ankle boss with its bearing, and a side lobe with the knee rod's bearing.

Frame: the STEP's (mm), seen from -y: the plane's x is the STEP's x, its y the STEP's z; depth is y,
from the back face (y 19) to the front face (y 43). The ankle's axis is along y through z 0, the
actuator's through z 154 and z 207. The part is front-view outlines extruded along y, then cut by
three tilted planes, each through a corner of the back plate at y 29: the planes are measured
(as dz per mm of y). Approximated: the side lobe's draft behind the front plate, in two steps.
Not drawn: the R3 fillets where the blocks meet the front plate's back face."""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)
M3 = S.M3

# -- interfaces -- fixed ----------------------------------------------------------------------------
# tibias2_tibias12, the other leg's, is this design mirrored about y 19 with its own holes: it runs
# this program with its TIBIA (the values in this part's frame, before the mirror)
TIBIA = globals().get("TIBIA", {})
ANKLE_AT = (0.0, 0.0)
ANKLE_SEAT = TIBIA.get("ankle_seat", ((21.0, 37.0, 43.0),))        # 15x21x4 bearing: d, from, to
ANKLE_SCREWS = TIBIA.get("ankle_screws")                           # d, circle d, first deg, count
MOTOR_AT = ((0.0, 154.0), (0.0, 207.0))   # the knee actuator's two pockets
MOTOR_POCKET = TIBIA.get("motor_pocket", {MOTOR_AT[0]: (46.0, 38.0, 41.0), MOTOR_AT[1]: (46.0, 32.3, 41.5)})   # d, from, to
MOTOR_BORE_D = 33.0                       # through the front face, both
KEY_W, KEY_AT = 2.0, TIBIA.get("key_at", MOTOR_AT[1])   # a bar across that bore, along z (its R2 corners not drawn); not in the model: the actuator's key (its mesh has none)
M3_RING = TIBIA.get("m3_ring", {MOTOR_AT[0]: (41.5, 22.5, 8, 41.0), MOTOR_AT[1]: (38.5, 37.0, 4, 41.5)})  # circle d, first deg, count, from y
PIN_D, PIN_PITCH, PIN_AT_Z = 3.5, 35.0, 180.5     # through the front plate
LOBE_AT = (-32.139, 221.698)              # the knee rod's bearing  # measured
LOBE_SEAT = TIBIA.get("lobe_seat", ((21.0, 31.0, 35.0), (19.0, 35.0, 38.0), (2.9, 38.0, 43.0)))   # d, from, to
BACK_HOLES = TIBIA.get("back_holes", ((3.8, 19.0, 29.0),))       # d, from, to: through the back plate
BACK_GRID, BACK_GRID_AT = (14.0, 25.7), (0.0, 81.17)             # measured
BACK_BOLT_D, BACK_BOLT_AT = 5.15, (0.0, 260.0)
DOWELS = ((3.0, (0.0, 50.0), 34.46), (3.0, (0.0, 243.4), 36.26))     # d, at, to y (blind from the back)
BACK = 19.0
LOBE_FROM = 31.0

# -- body: free -------------------------------------------------------------------------------------
ANKLE_FROM = 37.0                          # the ankle's boss, from y
CABLE_D = 5.0                              # a groove along z in the back face
CABLE_X = -12.5
CABLE_Z = (235.35, 252.96)
BACK_TO = 29.0
FRONT_FROM = 38.0
FRONT = 43.0
LOW_PLANE = (60.322, -2.1667)             # z at y 29, dz per mm of y  # measured
UP_PLANE = (102.016, 1.857)               # measured
TOP_PLANE = (251.502, -1.3216)            # measured

# the column, symmetric about x 0: half its width at its foot (on the ankle's block), along its waist (between
# the low and the up plane, where they meet the back plate) and at its shoulders (under the actuator's saddle)
COLUMN_FOOT_Z, COLUMN_TOP_Z = 30.0, 128.0
HALF_FOOT, HALF_WAIST, HALF_TOP = 18.13, 15.0, 28.1      # measured
Z_LOW, Z_UP = LOW_PLANE[0], UP_PLANE[0]

# outlines: ("line", corner) or ("arc", corner, centre, ccw). The rounds: R30.6 the column's saddle under the
# first actuator, R32.1 the top piece's under the second, R100 the front plate's side, R5 about the back bolt  # measured
COLUMN = [(-HALF_TOP, COLUMN_TOP_Z), ("line", (-28.84, 135.33)), ("arc", (-25.2, 136.66), (-26.85, 135.53), False),
          ("arc", (24.16, 135.24), MOTOR_AT[0], True), ("arc", (27.74, 134.13), (25.74, 134.02), False),
          ("line", (HALF_TOP, COLUMN_TOP_Z)), ("line", (HALF_WAIST, Z_UP)), ("line", (HALF_WAIST, Z_LOW)),
          ("line", (HALF_FOOT, COLUMN_FOOT_Z)), ("line", (-HALF_FOOT, COLUMN_FOOT_Z)), ("line", (-HALF_WAIST, Z_LOW)),
          ("line", (-HALF_WAIST, Z_UP))]
TOP_PIECE = [(-23.47, 230.29), ("line", (-4.35, 262.47)), ("arc", (4.3, 262.55), BACK_BOLT_AT, False),
             ("line", (21.45, 233.7)), ("arc", (18.6, 233.13), (19.76, 234.76), False),
             ("arc", (-22.59, 229.76), MOTOR_AT[1], True), ("arc", (-22.72, 229.65), (-24.0, 231.18), False),
             ("arc", (-23.47, 230.29), (-23.04, 230.03), False)]
ANKLE = [(HALF_FOOT, COLUMN_FOOT_Z), ("line", (14.92, -1.52)), ("arc", (-14.95, -1.17), ANKLE_AT, False),
         ("line", (-HALF_FOOT, COLUMN_FOOT_Z)), ("line", (-HALF_WAIST, Z_LOW)), ("line", (HALF_WAIST, Z_LOW))]
# -- interfaces -- fixed: the front plate's outline, on the actuator ----------------------------
FRONT_PLATE = [(21.86, 233.0), ("line", (14.73, 245.0)), ("line", (-18.75, 245.0)), ("line", (-18.75, 238.81)),
               ("arc", (-28.74, 233.21), (-26.48, 240.88), False), ("arc", (-39.08, 211.91), LOBE_AT, True),
               ("arc", (-35.71, 205.03), (-43.71, 205.38), False), ("arc", (-35.63, 202.13), (-15.73, 204.15), True),
               ("line", (-HALF_TOP, COLUMN_TOP_Z)), ("line", (-HALF_WAIST, Z_UP)), ("line", (HALF_WAIST, Z_UP)),
               ("line", (HALF_TOP, COLUMN_TOP_Z)), ("line", (26.78, 150.29)), ("arc", (26.69, 150.77), (24.78, 150.18), True),
               ("arc", (22.53, 189.06), (122.0, 180.5), False), ("arc", (23.8, 200.37), (30.09, 193.93), False)]

# -- body: free -------------------------------------------------------------------------------------

def profile(wp, outline):
    """An outline from its first corner, then lines and arcs about their centres."""
    wp = wp.moveTo(*outline[0])
    here = outline[0]
    for seg in outline[1:]:
        if seg[0] == "line":
            wp = wp.lineTo(*seg[1])
        else:
            _, end, (cx, cy), ccw = seg
            a0 = math.atan2(here[1] - cy, here[0] - cx)
            a1 = math.atan2(end[1] - cy, end[0] - cx)
            r0 = math.hypot(here[0] - cx, here[1] - cy)
            end = (cx + r0 * math.cos(a1), cy + r0 * math.sin(a1))   # on the arc's circle, whatever was measured
            sweep = (a1 - a0) % (2 * math.pi) if ccw else -((a0 - a1) % (2 * math.pi))
            r = r0
            wp = wp.threePointArc((cx + r * math.cos(a0 + sweep / 2), cy + r * math.sin(a0 + sweep / 2)), end)
        here = seg[1] if seg[0] == "line" else end
    return wp.close()


def at_y(y):
    """A plane at that y, seen from -y (x is x, y is the STEP's z); extrude(-d) goes d deeper in y."""
    return cq.Workplane(cq.Plane(origin=(0, y, 0), xDir=(1, 0, 0), normal=(0, -1, 0)))


def prism(outline, y0, y1):
    return profile(at_y(y0), outline).extrude(y0 - y1)


def side(points):
    """A side-view region, (y, z) points, through the whole part along x."""
    return cq.Workplane("YZ", origin=(-60, 0, 0)).polyline(points).close().extrude(120)


def plane_z(plane, y):
    return plane[0] + plane[1] * (y - BACK_TO)


tibia = prism(COLUMN, BACK, FRONT)
tibia = tibia.union(prism(TOP_PIECE, BACK, FRONT_FROM))
tibia = tibia.union(prism(ANKLE, ANKLE_FROM, FRONT))
tibia = tibia.union(prism(FRONT_PLATE, FRONT_FROM, FRONT))
# the lobe reaches back to LOBE_FROM, drafted: the front plate's outline, left of an inner edge and
# above an underside that both move out with depth -- drawn in two steps, each read at its middle
LOBE_STEPS = [(LOBE_FROM, LOBE_SEAT[0][2], ((-37.35, 210.25), (-21.66, 214.72)), -20.0),   # y from, to, underside, inner x
              (LOBE_SEAT[0][2], FRONT_FROM, ((-35.99, 207.5), (-22.75, 210.38)), -17.4)]   # measured
lobe = None
for y0, y1, ((ux0, uz0), (ux1, uz1)), inner in LOBE_STEPS:
    k = (uz1 - uz0) / (ux1 - ux0)
    under = [(-60, uz0 + k * (-60 - ux0)), (inner, uz0 + k * (inner - ux0)), (inner, 300), (-60, 300)]
    step = prism(FRONT_PLATE, y0, y1).intersect(at_y(y0 - 1).polyline(under).close().extrude(y0 - y1 - 2))
    lobe = step if lobe is None else lobe.union(step)
tibia = tibia.union(lobe)

# the three planes: open between the low and the up plane, nothing above the top plane, past y 29
far = FRONT + 1
tibia = tibia.cut(side([(BACK_TO, plane_z(LOW_PLANE, BACK_TO)), (BACK_TO, plane_z(UP_PLANE, BACK_TO)),
                        (far, plane_z(UP_PLANE, far)), (far, plane_z(LOW_PLANE, far))]))
tibia = tibia.cut(side([(BACK_TO, plane_z(TOP_PLANE, BACK_TO)), (far, plane_z(TOP_PLANE, far)), (far, 300), (BACK_TO, 300)]))

# the actuator's pockets and bores, its screws, the pins
for at, (d, y0, y1) in MOTOR_POCKET.items():
    tibia = tibia.cut(at_y(y0).center(*at).circle(d / 2).extrude(y0 - y1))
    tibia = tibia.cut(at_y(y1).center(*at).circle(MOTOR_BORE_D / 2).extrude(y1 - far))
key_from = MOTOR_POCKET[KEY_AT][2]
tibia = tibia.union(at_y(key_from).center(*KEY_AT).rect(KEY_W, MOTOR_BORE_D).extrude(key_from - FRONT))
for at, (cd, first, n, y0) in M3_RING.items():
    tibia = tibia.cut(at_y(y0).center(*at).polarArray(cd / 2, first, 360, n).circle(M3.hole_d / 2).extrude(y0 - far))
tibia = tibia.cut(at_y(FRONT_FROM).center(0, PIN_AT_Z).rarray(PIN_PITCH, 1, 2, 1).circle(PIN_D / 2).extrude(FRONT_FROM - far))

# the bearings: the ankle's, through; the lobe's, stepped
for d, y0, y1 in ANKLE_SEAT:
    tibia = tibia.cut(at_y(y0).center(*ANKLE_AT).circle(d / 2).extrude(y0 - (far if y1 >= FRONT else y1)))
if ANKLE_SCREWS:
    d, cd, first, n = ANKLE_SCREWS
    tibia = tibia.cut(at_y(ANKLE_FROM).center(*ANKLE_AT).polarArray(cd / 2, first, 360, n).circle(d / 2).extrude(ANKLE_FROM - far))
for d, y0, y1 in LOBE_SEAT:
    tibia = tibia.cut(at_y(y0).center(*LOBE_AT).circle(d / 2).extrude(y0 - y1))

# from the back: the grid, the bolt, the dowels, the cable groove
for d, y0, y1 in BACK_HOLES:
    tibia = tibia.cut(at_y(y0).center(*BACK_GRID_AT).rarray(*BACK_GRID, 2, 2).circle(d / 2).extrude(y0 - y1))
tibia = tibia.cut(at_y(BACK).center(*BACK_BOLT_AT).circle(BACK_BOLT_D / 2).extrude(BACK - BACK_TO))
for d, at, y1 in DOWELS:
    tibia = tibia.cut(at_y(BACK).center(*at).circle(d / 2).extrude(BACK - y1))
# the groove's tool reaches out behind the back face: an axis lying in the face cuts nothing in OCC
groove = cq.Sketch().push([(CABLE_X, BACK)]).circle(CABLE_D / 2).push([(CABLE_X, BACK - CABLE_D / 2)]).rect(CABLE_D, CABLE_D)
tibia = tibia.cut(cq.Workplane("XY", origin=(0, 0, CABLE_Z[0])).placeSketch(groove).extrude(CABLE_Z[1] - CABLE_Z[0]))
result = tibia.mirror("XZ", (0, TIBIA["mirror_about_y"], 0)) if "mirror_about_y" in TIBIA else tibia
