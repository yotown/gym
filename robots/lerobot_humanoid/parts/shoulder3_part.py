"""Robot-arm shoulder: a d35 shaft along x (x -91.593 to -51.593) with an r4 fillet into a 35x35 square
arm. The arm flares with r12.5 arcs into a clevis fork: two 2 mm plates at y 26..28 and y -28..-26,
each a d61 half-disk (x <= 0) joined to the arm strip by r12.5 arcs. Between the plates is a d61
cylindrical cavity. The +y plate has a d41 hole and three M3 holes on r25. The -y plate has two M3
holes on r19 and a d18/d15 servo boss with three blind d2.3 holes. Six M3 screw bores on r13.5 run
along x: d3.3 through the 5 mm end cap, then d6 up to the cavity. Frame: the STEP's; the shaft along x, the fork's axis along y through the origin.
The r1 rounds on the cusps where the cavity wall meets the r12.5 flares are cut as
exact 2D profiles. The r1 rounds on the plate rims are fillets.
Not reproduced: the concave r1 fillets between the cavity wall and the plates (tori 90/93) and the
freeform patches where the r5 arm-edge rounds cross the flare arcs (the r5 rounds stop there)."""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)
M3 = S.M3

# -- interfaces -- fixed ----------------------------------------------------------------------------
# the shoulder bearing on the shaft, and six screws along it into the next part
X_END = -91.593                            # the shaft's end face
X_SHOULDER = -51.593                       # the shaft's shoulder, the bearing's stop; not in the model: the bearing
SHAFT_D = 35.0                             # bearing 35; not in the model: the bearing
SCREW_CIRCLE_R = 13.5                      # the screws, on this circle about the shaft's axis,
SCREW_FIRST_DEG = 30.0
SCREW_COUNT = 6
SCREW_HEAD_D = 6.0                         # counterbored from the fork's cavity,
SCREW_HEAD_SEAT = 5.0                      # the heads seated this far in from the end face
# the fork: the motor between its plates
FORK_R = 30.5                              # the cavity between the plates, round the motor; the plates' disk the same
PLATE_Y = 28.0                             # their outer faces, against the forearm
PLATE_SCREW_D = 3.3                        # M3 through the plates:
PLUS_SCREW_R = 25.0                        # the +y plate's, on this circle,
PLUS_SCREW_DEG = (120.0, 180.0, 240.0)     # at these angles (from +x, about the fork's axis)
MINUS_SCREW_R = 19.0                       # the -y plate's,
MINUS_SCREW_DEG = (135.0, 225.0)
# the boss on the -y plate: its end and the screws into it
SPIGOT_TO_Y = 33.9                         # the boss's end (|y|)
HORN_SCREW_R = 4.0                         # three screws into it, on this circle about the fork's axis,
HORN_SCREW_FIRST_DEG = -30.0
HORN_SCREW_COUNT = 3
HORN_SCREW_D = 2.3

# -- body: free -------------------------------------------------------------------------------------
FORK_INNER_Y = 26.0                        # the plates' inner faces, each side: clear of the motor
CENTRE_HOLE_D = 41.0                       # through the +y plate, on the fork's axis
BOSS_D = 18.0                              # the boss on the -y plate, out to
BOSS_TO_Y = 30.0                           # this |y|;
SPIGOT_D = 15.0                            # then a spigot, to the boss's end
HORN_SCREW_DEEP = 5.0                      # the screws' blind holes
ARM_H = 17.5                               # the square arm's half width
FLARE_R = 12.5                             # the arm flaring out into the fork
EDGE_R = 1.0                               # small rounds on the fork
ARM_ROUND_R = 5.0                          # the arm's four long edges
SHAFT_FILLET_R = 4.0                       # the shaft into the arm

PLATE_T = PLATE_Y - FORK_INNER_Y           # the plates' thickness
inner_y = FORK_INNER_Y

# ---- fork profile in XZ (disk + arm strip with r12.5 concave flares), swept along y
zc = ARM_H + FLARE_R
xc = -math.sqrt((FORK_R + FLARE_R) ** 2 - zc ** 2)   # -30.806
a_t = math.atan2(zc, xc)                              # tangent direction on the disk


def P(cx, cy, r, ang):
    return (cx + r * math.cos(ang), cy + r * math.sin(ang))


T_top = P(0, 0, FORK_R, a_t)
T_bot = (T_top[0], -T_top[1])
m_fil_bot = P(xc, -zc, FLARE_R, (math.pi / 2 + math.pi - a_t) / 2)
m_disk_bot = P(0, 0, FORK_R, (-a_t - math.pi / 2) / 2)
m_disk_top = P(0, 0, FORK_R, (math.pi / 2 + a_t) / 2)
m_fil_top = P(xc, zc, FLARE_R, (a_t - math.pi - math.pi / 2) / 2)

pxz = (cq.Workplane("XZ", origin=(0, PLATE_Y, 0))
       .moveTo(X_SHOULDER, -ARM_H).lineTo(xc, -ARM_H)
       .threePointArc(m_fil_bot, T_bot)
       .threePointArc(m_disk_bot, (0, -FORK_R))
       .lineTo(0, FORK_R)
       .threePointArc(m_disk_top, T_top)
       .threePointArc(m_fil_top, (xc, ARM_H))
       .lineTo(X_SHOULDER, ARM_H).close()
       .extrude(2 * PLATE_Y))

# ---- plan profile in XY (arm flaring with r12.5 arcs out to the plates), swept along z
yc = ARM_H + FLARE_R
xfy = xc - math.sqrt(FLARE_R ** 2 - (yc - PLATE_Y) ** 2)   # -43.145
b = math.atan2(yc - PLATE_Y, xc - xfy)
pxy = (cq.Workplane("XY", origin=(0, 0, -FORK_R))
       .moveTo(X_SHOULDER, -ARM_H).lineTo(xfy, -ARM_H)
       .threePointArc(P(xfy, -yc, FLARE_R, (math.pi / 2 + b) / 2), (xc, -PLATE_Y))
       .lineTo(0, -PLATE_Y).lineTo(0, PLATE_Y).lineTo(xc, PLATE_Y)
       .threePointArc(P(xfy, yc, FLARE_R, -(math.pi / 2 + b) / 2), (xfy, ARM_H))
       .lineTo(X_SHOULDER, ARM_H).close()
       .extrude(2 * FORK_R))

body = pxz.intersect(pxy)

# r5 rounds on the four arm edges
s_top = cq.selectors.BoxSelector((X_SHOULDER + 0.5, -PLATE_Y - 1, ARM_H - 0.5), (xc - 0.5, PLATE_Y + 1, ARM_H + 0.5))
s_bot = cq.selectors.BoxSelector((X_SHOULDER + 0.5, -PLATE_Y - 1, -ARM_H - 0.5), (xc - 0.5, PLATE_Y + 1, -ARM_H + 0.5))
body = body.edges(cq.selectors.SumSelector(s_top, s_bot)).fillet(ARM_ROUND_R)

# ---- d35 shaft and its r4 shoulder fillet (tori 95-98)
shaft = cq.Workplane("YZ", origin=(X_END, 0, 0)).circle(SHAFT_D / 2).extrude(X_SHOULDER - X_END)
body = body.union(shaft)
# the shaft's r4 fillet into the arm: a ring less a torus, kept inside the rounded square
xr = X_SHOULDER - SHAFT_FILLET_R
ring = (cq.Workplane("YZ", origin=(xr, 0, 0)).circle(SHAFT_D / 2 + SHAFT_FILLET_R).extrude(SHAFT_FILLET_R)
        .cut(cq.Solid.makeTorus(SHAFT_D / 2 + SHAFT_FILLET_R, SHAFT_FILLET_R, cq.Vector(xr, 0, 0), cq.Vector(1, 0, 0))))
square = cq.Workplane("YZ", origin=(xr, 0, 0)).rect(2 * ARM_H, 2 * ARM_H).extrude(SHAFT_FILLET_R).edges("|X").fillet(ARM_ROUND_R)
body = body.union(ring.intersect(square))

# ---- the cavity between the plates
body = body.cut(cq.Workplane("XZ", origin=(0, inner_y, 0)).circle(FORK_R).extrude(2 * inner_y))

# ---- r1 rounds on the cusps where the cavity wall is tangent to the xz flares.
# The round centre is EDGE_R outside both circles. Cut the cusp tip beyond the round; the chord
# back to the disk tangent point runs through the empty cavity.
dOF = math.hypot(xc, zc)
ux, uz = xc / dOF, zc / dOF
r1c, r2c = FORK_R + EDGE_R, FLARE_R + EDGE_R
aa = (r1c ** 2 - r2c ** 2 + dOF ** 2) / (2 * dOF)
hh = math.sqrt(r1c ** 2 - aa ** 2)
Cx, Cz = aa * ux - hh * uz, aa * uz + hh * ux                 # (-26.353, 17.255)
Ax, Az = Cx * FORK_R / r1c, Cz * FORK_R / r1c                 # tangent on cavity wall
Bx, Bz = xc + (Cx - xc) * FLARE_R / r2c, zc + (Cz - zc) * FLARE_R / r2c   # tangent on flare
Tx, Tz = ux * FORK_R, uz * FORK_R                             # disk/flare tangent point
dl = math.hypot(Tx - Cx, Tz - Cz)
Rmx, Rmz = Cx + EDGE_R * (Tx - Cx) / dl, Cz + EDGE_R * (Tz - Cz) / dl
bx, bz = (Bx - xc) + (Tx - xc), (Bz - zc) + (Tz - zc)
bl = math.hypot(bx, bz)
Fmx, Fmz = xc + FLARE_R * bx / bl, zc + FLARE_R * bz / bl
cusp = cq.Workplane("XZ", origin=(0, inner_y, 0))
for s in (1, -1):
    cusp = (cusp.moveTo(Ax, s * Az).threePointArc((Rmx, s * Rmz), (Bx, s * Bz))
            .threePointArc((Fmx, s * Fmz), (Tx, s * Tz)).close())
body = body.cut(cusp.extrude(2 * inner_y))

# ---- the plates' holes: the centre hole and the screws
def on_circle(r, degs):
    return [P(0, 0, r, math.radians(a)) for a in degs]


body = body.cut(cq.Workplane("XZ", origin=(0, PLATE_Y + 1, 0)).circle(CENTRE_HOLE_D / 2).extrude(PLATE_T + 2))
body = body.cut(cq.Workplane("XZ", origin=(0, PLATE_Y + 1, 0)).pushPoints(on_circle(PLUS_SCREW_R, PLUS_SCREW_DEG))
                .circle(PLATE_SCREW_D / 2).extrude(PLATE_T + 2))
body = body.cut(cq.Workplane("XZ", origin=(0, -inner_y + 1, 0)).pushPoints(on_circle(MINUS_SCREW_R, MINUS_SCREW_DEG))
                .circle(PLATE_SCREW_D / 2).extrude(PLATE_T + 2))

# ---- the horn's boss on -y, and its screws
body = body.union(cq.Workplane("XZ", origin=(0, -inner_y, 0)).circle(BOSS_D / 2).extrude(BOSS_TO_Y - inner_y))
body = body.union(cq.Workplane("XZ", origin=(0, -BOSS_TO_Y, 0)).circle(SPIGOT_D / 2).extrude(SPIGOT_TO_Y - BOSS_TO_Y))
step = 360.0 / HORN_SCREW_COUNT
body = body.cut(cq.Workplane("XZ", origin=(0, -(SPIGOT_TO_Y - HORN_SCREW_DEEP), 0))
                .pushPoints(on_circle(HORN_SCREW_R, [HORN_SCREW_FIRST_DEG + k * step for k in range(HORN_SCREW_COUNT)]))
                .circle(HORN_SCREW_D / 2).extrude(HORN_SCREW_DEEP + 1))

# ---- the screws along the shaft: through the end, counterbored from the cavity
step = 360.0 / SCREW_COUNT
pts_s = on_circle(SCREW_CIRCLE_R, [SCREW_FIRST_DEG + k * step for k in range(SCREW_COUNT)])
x_seat = X_END + SCREW_HEAD_SEAT
body = body.cut(cq.Workplane("YZ", origin=(X_END - 1, 0, 0)).pushPoints(pts_s).circle(M3.hole_d / 2)
                .extrude(SCREW_HEAD_SEAT + 1.5))
body = body.cut(cq.Workplane("YZ", origin=(x_seat, 0, 0)).pushPoints(pts_s).circle(SCREW_HEAD_D / 2)
                .extrude(-x_seat))

# ---- r1 rounds on the outer rims of the plates (tori 75/81/82/88 on the disk arcs,
# tori 76/80/83/87 on the flares, cylinders 78/85 at the plan-flare corner)
def _rim_edges(solid, yface):
    out = []
    for e in solid.Edges():
        bb = e.BoundingBox()
        if abs(bb.ymin - yface) > 1e-3 or abs(bb.ymax - yface) > 1e-3:
            continue
        gt = e.geomType()
        if gt == "CIRCLE":
            r = e.radius()
            if abs(r - FORK_R) < 1e-3 or abs(r - FLARE_R) < 1e-3:
                out.append(e)
        elif gt == "LINE" and abs(bb.xmin - xc) < 1e-3 and abs(bb.xmax - xc) < 1e-3:
            out.append(e)
    return out


solid = body.val()
for yface in (PLATE_Y, -PLATE_Y):
    solid = solid.fillet(EDGE_R, _rim_edges(solid, yface))

result = cq.Workplane("XY").add(solid)
