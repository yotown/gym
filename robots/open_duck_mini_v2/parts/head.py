"""Open Duck Mini v2 head, written from its STEP: interfaces exact, the body simple.

A shell open underneath, on the bottom sheet. Its cavity is bounded by flat faces (front, top, back, the
sides leaning in, chamfers between the sides and the top) -- the bottom sheet fits inside it -- and its
wall is WALL thick outside that; under the top the chamfers are thicker. Inside: screw bosses round the
rim, the plate at the back that takes the head roll mount, two eye holes in the front, and bosses under
the top for the boards.

Frame: the vendor's (mm): x forward, z up; the head is symmetric about y = 0. A face is given by its outward
normal (azimuth, elevation, deg) and its level: its distance from the origin.
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
CAVITY_FRONT_X = 117.0                     # the cavity: its front,
CAVITY_TOP_Z = 166.11                      # its top,
CAVITY_FACES = [(180.0, 9.555, 94.103),    # the back,  # measured
                (105.71, 13.663, 94.474),  # the sides behind the eyes, leaning in,  # measured
                (97.99, 16.98, 112.035),   # between them and  # measured
                (90.0, 20.0, 127.553),     # the sides by the eyes,  # measured
                (180.0, 77.47, 157.744),   # the top's back slope,  # measured
                (117.16, 49.07, 157.341),  # the chamfers between the sides and the top  # measured
                (105.71, 51.84, 165.922),  # measured
                (98.75, 50.21, 169.742),   # measured
                (90.0, 55.0, 179.337)]     # measured
RIM_SCREWS = [(4.061, 62.06), (-68.391, 44.501), (105.0, 69.0), (80.0, 84.0)]   # up into the rim, each and its mirror in y
RIM_INSERT_D = 4.0                         # each into an insert,
RIM_INSERT_DEEP = 8.8                      # this deep above the rim,
RIM_SCREW_D = 3.2                          # and its screw on
NECK_X = (-30.0, -21.0)                    # the head roll mount's plate: x from-to,
NECK_Z = 129.06                            # its axis's z,
NECK_BORE_D = 28.0                         # through it,
NECK_CBORE_D = 32.2                        # counterbored
NECK_LIP = 1.9                             # from this far behind the plate's back
EYE_Y = 40.0                               # through the front: |y|,
EYE_Z = 139.41
EYE_D = 25.0
EYE_SCREW_Y = (27.5, 52.5)                 # round each eye: |y|,
EYE_SCREW_Z = (126.91, 151.91)
EYE_SCREW_D = 2.7
LIGHT_Z = 153.11                           # through the front on the middle
LIGHT_D = 7.75
FRONT_BOSS_Y = (0.0, -12.5)                # inside the front: y,
FRONT_BOSS_Z = (142.61, 163.61)            # z,
FRONT_BOSS_HOLE_D = 1.65
TOP_SCREW_X = (65.0, 95.0)                 # under the top: x,
TOP_SCREW_Y = 27.37                        # |y|,
TOP_INSERT_D = 4.0                         # each an insert
TOP_INSERT_SHORT = 1.3                     # stopping this short of the cavity's top,
TOP_SCREW_D = 3.2                          # then the screw's hole
BOSS_BOTTOM_Z = 159.01                     # the top's bosses run down to here
STANDOFF_RECT_X = (25.975, 84.025)         # the boards' standoffs under the top: a rectangle on +y (x, y),
STANDOFF_RECT_Y = (36.475, 59.525)
STANDOFF_PAIRS = [[(63.287, -41.933), (61.121, -49.634)], [(32.482, -33.269), (30.316, -40.97)]]   # and two pairs joined, on -y
STANDOFF_Z = 161.11                        # down to here
STANDOFF_HOLE_D = 2.0
CHAMFER_EXTRA = [0.0, 0.0, 0.0, 0.0, 0.0, 4.949, 5.423, 5.0, 4.409]   # by this much inside: the boards against them (each of CAVITY_FACES)  # measured
NECK_HALF_W = 19.0                         # the neck plate: half its width (its round bottom's r), by the bottom sheet
RIM_BOSS_FROM = 3.0                        # the rim screws' bosses start this far above the rim: the bottom sheet against them
TOP_RECESS_X = (59.9, 100.1)               # in the top's underside between its bosses, round the roll mount's top: x,
TOP_RECESS_HALF_Y = 19.47
TOP_RECESS_DEEP = 1.0

# -- body: free -------------------------------------------------------------------------------------
BACK_SHELF = (180.0, 43.51, 147.347)       # the cavity closed under the top's back slope by this face  # measured
RIM_SCREW_DEEP = 13.0                      # the rim screws run this far above the rim
FRONT_BOSS_LONG = 3.2                       # the bosses inside the front: long,
FRONT_BOSS_D = 5.0
WALL = 3.0                                 # outside the cavity
THICK_FROM = 161.11                        # from here up the chamfers are thicker,
NECK_TOP_X = (-36.07, -17.1)               # where it widens to the top: x,
NECK_TOP_HALF_Y = 23.99                    # half y,
NECK_TOP_FROM_Z = 148.71                   # from z,
NECK_TOP_FACES = ((180.0, -51.27, -97.228), (0.0, -38.74, -112.071))   # its sloped faces  # measured
RIM_BOSS_D = 8.0                           # the rim screws' bosses
RIM_WEB_DEG = [105.71, 140.71, 0.0, 90.0]  # each webbed to the wall this way (deg)
TOP_BOSS_D = 10.0
STANDOFF_D = 7.5                           # the rectangle's, and the pairs' width
STANDOFF_PAIR_W = 10.0

TOP_Z, FRONT_X = CAVITY_TOP_Z + WALL, CAVITY_FRONT_X + WALL


def beyond(az, el, level):
    """Everything beyond a face: its outward normal at azimuth az and elevation el, level from the origin."""
    a, e = math.radians(az), math.radians(el)
    n = cq.Vector(math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))
    x = n.cross(cq.Vector(0, 0, 1)) if abs(n.z) < 0.99 else cq.Vector(1, 0, 0)
    return cq.Workplane(cq.Plane(origin=n * level, xDir=x, normal=n)).rect(2000, 2000).extrude(1000)


def bounded(front, top, levels, below=0.0):
    """A block cut back to the faces at these levels (each face and its mirror in y)."""
    body = cq.Workplane("XY", origin=(0, 0, S.HEAD_RIM_Z - below)).rect(2 * front, 400).extrude(top - S.HEAD_RIM_Z + below)
    for (az, el, _), level in zip(CAVITY_FACES + [BACK_SHELF], levels):
        if level is None:
            continue
        for s in ((1, -1) if az % 180 else (1,)):
            body = body.cut(beyond(s * az, el, level))
    return body


inner = [lv for _, _, lv in CAVITY_FACES]
outer = bounded(FRONT_X, TOP_Z, [lv + WALL for lv in inner] + [None])
cavity = bounded(CAVITY_FRONT_X, CAVITY_TOP_Z, [lv - e for lv, e in zip(inner, CHAMFER_EXTRA)] + [BACK_SHELF[2]], below=1.0)
cavity_low = bounded(CAVITY_FRONT_X, CAVITY_TOP_Z, inner + [BACK_SHELF[2]], below=1.0)
shell = outer.cut(cavity).cut(cavity_low.intersect(cq.Workplane("XY", origin=(0, 0, S.HEAD_RIM_Z - 1)).rect(400, 400).extrude(THICK_FROM - S.HEAD_RIM_Z + 1)))
rx0, rx1 = TOP_RECESS_X
shell = shell.cut(cq.Workplane("XY", origin=(0, 0, CAVITY_TOP_Z - 1)).center((rx0 + rx1) / 2, 0).rect(rx1 - rx0, 2 * TOP_RECESS_HALF_Y).extrude(1 + TOP_RECESS_DEEP))

# -- interfaces -------------------------------------------------------------------------------------
webs = cq.Workplane("XY")
for (x, y), deg in zip(RIM_SCREWS, RIM_WEB_DEG):
    for s in (1, -1):
        webs = webs.union(cq.Workplane("XY", origin=(x, s * y, S.HEAD_RIM_Z + RIM_BOSS_FROM)).transformed(rotate=(0, 0, s * deg))
                          .center(25, 0).rect(50, RIM_BOSS_D).extrude(TOP_Z - S.HEAD_RIM_Z))
pts = [(x, s * y) for x, y in RIM_SCREWS for s in (1, -1)]
shell = shell.union(cq.Workplane("XY", origin=(0, 0, S.HEAD_RIM_Z + RIM_BOSS_FROM)).pushPoints(pts).circle(RIM_BOSS_D / 2).extrude(TOP_Z - S.HEAD_RIM_Z).union(webs).intersect(outer))
shell = shell.cut(cq.Workplane("XY", origin=(0, 0, S.HEAD_RIM_Z)).pushPoints(pts).circle(RIM_INSERT_D / 2).extrude(RIM_INSERT_DEEP))
shell = shell.cut(cq.Workplane("XY", origin=(0, 0, S.HEAD_RIM_Z)).pushPoints(pts).circle(RIM_SCREW_D / 2).extrude(RIM_SCREW_DEEP))

nx0, nx1 = NECK_X
plate = cq.Workplane("YZ", origin=(nx0, 0, 0)).center(0, NECK_Z).circle(NECK_HALF_W).extrude(nx1 - nx0)
plate = plate.union(cq.Workplane("YZ", origin=(nx0, 0, 0)).center(0, (NECK_Z + TOP_Z) / 2).rect(2 * NECK_HALF_W, TOP_Z - NECK_Z).extrude(nx1 - nx0)).intersect(outer)
gx0, gx1 = NECK_TOP_X
gusset = cq.Workplane("XY", origin=(0, 0, NECK_TOP_FROM_Z)).center((gx0 + gx1) / 2, 0).rect(gx1 - gx0, 2 * NECK_TOP_HALF_Y).extrude(TOP_Z - NECK_TOP_FROM_Z)
for face in NECK_TOP_FACES:
    gusset = gusset.cut(beyond(*face))
shell = shell.union(plate).union(gusset.intersect(outer))
shell = shell.cut(cq.Workplane("YZ", origin=(nx0 - 1, 0, 0)).center(0, NECK_Z).circle(NECK_BORE_D / 2).extrude(nx1 - nx0 + 2))
shell = shell.cut(cq.Workplane("YZ", origin=(nx0 + NECK_LIP, 0, 0)).center(0, NECK_Z).circle(NECK_CBORE_D / 2).extrude(nx1 - nx0))

front = cq.Workplane("YZ", origin=(CAVITY_FRONT_X - 1, 0, 0))
shell = shell.cut(front.pushPoints([(s * EYE_Y, EYE_Z) for s in (1, -1)]).circle(EYE_D / 2).extrude(WALL + 2))
shell = shell.cut(front.pushPoints([(s * y, z) for y in EYE_SCREW_Y for z in EYE_SCREW_Z for s in (1, -1)]).circle(EYE_SCREW_D / 2).extrude(WALL + 2))
shell = shell.cut(front.center(0, LIGHT_Z).circle(LIGHT_D / 2).extrude(WALL + 2))
fp = [(y, z) for y in FRONT_BOSS_Y for z in FRONT_BOSS_Z]
shell = shell.union(cq.Workplane("YZ", origin=(CAVITY_FRONT_X - FRONT_BOSS_LONG, 0, 0)).pushPoints(fp).circle(FRONT_BOSS_D / 2).extrude(FRONT_BOSS_LONG + 0.5))
shell = shell.cut(cq.Workplane("YZ", origin=(CAVITY_FRONT_X - FRONT_BOSS_LONG - 1, 0, 0)).pushPoints(fp).circle(FRONT_BOSS_HOLE_D / 2).extrude(FRONT_BOSS_LONG + 1))

tp = [(x, s * TOP_SCREW_Y) for x in TOP_SCREW_X for s in (1, -1)]
shell = shell.union(cq.Workplane("XY", origin=(0, 0, BOSS_BOTTOM_Z)).pushPoints(tp).circle(TOP_BOSS_D / 2).extrude(TOP_Z - BOSS_BOTTOM_Z).intersect(outer))
shell = shell.cut(cq.Workplane("XY", origin=(0, 0, BOSS_BOTTOM_Z - 1)).pushPoints(tp).circle(TOP_INSERT_D / 2).extrude(CAVITY_TOP_Z - BOSS_BOTTOM_Z + 1 - TOP_INSERT_SHORT))
shell = shell.cut(cq.Workplane("XY", origin=(0, 0, BOSS_BOTTOM_Z - 1)).pushPoints(tp).circle(TOP_SCREW_D / 2).extrude(CAVITY_TOP_Z - BOSS_BOTTOM_Z + 1))

under = cq.Workplane("XY", origin=(0, 0, STANDOFF_Z))
for x in STANDOFF_RECT_X:
    for y in STANDOFF_RECT_Y:
        shell = shell.union(under.center(x, y).circle(STANDOFF_D / 2).extrude(TOP_Z - STANDOFF_Z).intersect(outer))
        shell = shell.cut(under.center(x, y).circle(STANDOFF_HOLE_D / 2).extrude(CAVITY_TOP_Z - STANDOFF_Z))
for a, b in STANDOFF_PAIRS:
    run, deg = math.dist(a, b), math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    shell = shell.union(under.center((a[0] + b[0]) / 2, (a[1] + b[1]) / 2).slot2D(run + STANDOFF_PAIR_W, STANDOFF_PAIR_W, deg)
                        .extrude(TOP_Z - STANDOFF_Z).intersect(outer))
    shell = shell.cut(under.pushPoints([a, b]).circle(STANDOFF_HOLE_D / 2).extrude(CAVITY_TOP_Z - STANDOFF_Z))

result = shell
