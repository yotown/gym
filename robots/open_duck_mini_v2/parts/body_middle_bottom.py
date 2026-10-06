"""Open Duck Mini v2 body middle (the bottom half), written from its STEP: interfaces exact, the body simple.

A shell of the body's section (as body_front's) below the split line, its side walls open in the middle
for the legs; a thick floor under them (its underside sloping up at the back into a thin plate), four
screws up through it into the trunk, counterbored from below; near each end a frame inside, and four
bosses taking the front and back plates' screws.

Frame: the vendor's (mm): the shell runs along x from the back's joint to the front plate's; the section
in (y, z); the floor screws on a rectangle about x = y = 0.
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)
INSERT = S.INSERT

# -- interfaces -- fixed ----------------------------------------------------------------------------
SCREW_YZ = [(45.0, -22.313), (45.0, -62.033)]   # the plates' screws into the bosses, each and its mirror in y
TRUNK_SEAT_Z = -88.775                     # the floor's top: the trunk stands on it
FLOOR_SCREW_D = 3.2
FLOOR_SCREW_HEAD_D = 6.5
FLOOR_SCREW_HEAD_SEAT = 4.225              # below the trunk's seat

# -- body: free -------------------------------------------------------------------------------------
WALL = 3.0
LEG_OPENING_X = (-35.0, 35.0)              # the side walls are open between, above the floor
SLOPE_DEG = 16.7                           # the floor's underside rises at the back,  # measured
SLOPE_FROM_X = -35.0                       # from here back
BOSS_D = 8.0
WALL_Y = S.BODY_SECTION[0][0] - WALL / 2          # the side wall's middle (y): the screw bosses are joined to it
BOTTOM_Z = S.BODY_SECTION[5][1]                   # the skin's bottom


def section(inset):
    wp = cq.Workplane("YZ", origin=(S.BODY_BACK_JOINT_X, 0, 0)).polyline(S.BODY_SECTION).close()
    return wp.offset2D(-inset, "intersection") if inset else wp


def prism(inset, x0, x1, z_top=S.BODY_SPLIT_Z):
    below = cq.Workplane("XY", origin=(0, 0, -200)).center((x0 + x1) / 2, 0).rect(x1 - x0, 200).extrude(z_top + 200)
    return section(inset).extrude(S.BODY_FRONT_JOINT_X - S.BODY_BACK_JOINT_X).intersect(below)


bottom = prism(0, S.BODY_BACK_JOINT_X, S.BODY_FRONT_JOINT_X).cut(prism(WALL, S.BODY_BACK_JOINT_X - 1, S.BODY_FRONT_JOINT_X + 1))
o0, o1 = LEG_OPENING_X
bottom = bottom.cut(cq.Workplane("XY", origin=(0, 0, TRUNK_SEAT_Z)).center((o0 + o1) / 2, 0).rect(o1 - o0, 200).extrude(S.BODY_SPLIT_Z - TRUNK_SEAT_Z + 1))
# the floor: solid up to the trunk's seat, or up to the sloped plate's inner face where that is higher; nothing
# below the sloped underside at the back
k = math.tan(math.radians(SLOPE_DEG))
lift = WALL / math.cos(math.radians(SLOPE_DEG))
far = S.BODY_BACK_JOINT_X - 1
low = cq.Workplane("XY", origin=(0, 0, -200)).rect(400, 400).extrude(TRUNK_SEAT_Z + 200)
low = low.union(cq.Workplane("XZ", origin=(0, 200, 0)).polyline([(SLOPE_FROM_X, BOTTOM_Z + lift), (far, BOTTOM_Z + lift + k * (SLOPE_FROM_X - far)),
                                                                   (far, -200), (SLOPE_FROM_X, -200)]).close().extrude(400))
bottom = bottom.union(prism(WALL - 0.01, S.BODY_BACK_JOINT_X, S.BODY_FRONT_JOINT_X).intersect(low))
under = cq.Workplane("XZ", origin=(0, 200, 0)).polyline([(SLOPE_FROM_X, BOTTOM_Z), (far, BOTTOM_Z + k * (SLOPE_FROM_X - far)),
                                                         (far, -200), (SLOPE_FROM_X, -200)]).close().extrude(400)
bottom = bottom.cut(under)
frames = [(S.BODY_BACK_JOINT_X + S.BODY_FRAME_IN, S.BODY_BACK_JOINT_X + S.BODY_FRAME_IN + S.BODY_FRAME_T), (S.BODY_FRONT_JOINT_X - S.BODY_FRAME_IN - S.BODY_FRAME_T, S.BODY_FRONT_JOINT_X - S.BODY_FRAME_IN)]
for x0, x1 in frames:
    bottom = bottom.union(prism(WALL - 0.01, x0, x1).cut(prism(WALL + S.BODY_FRAME_W, x0 - 1, x1 + 1)))

# -- interfaces, cut last -------------------------------------------------------------------------
pts = [(s * y, z) for y, z in SCREW_YZ for s in (1, -1)]
reach = S.BODY_FRAME_IN + S.BODY_FRAME_T                 # each boss runs from the joint to the frame's far side
for end, inward in ((S.BODY_BACK_JOINT_X, 1), (S.BODY_FRONT_JOINT_X, -1)):
    wp = cq.Workplane("YZ", origin=(end, 0, 0))
    bottom = bottom.union(wp.pushPoints(pts).circle(BOSS_D / 2).extrude(inward * reach))
    # each boss out to the side wall, its own width: it would only touch the frame's inner face
    pads = [(math.copysign((abs(y) + WALL_Y) / 2, y), z) for y, z in pts]
    bottom = bottom.union(wp.pushPoints(pads).rect(WALL_Y - abs(pts[0][0]), BOSS_D).extrude(inward * reach))
    bottom = bottom.cut(wp.pushPoints(pts).circle(INSERT.hole_d / 2).extrude(inward * INSERT.depth))
    bottom = bottom.cut(wp.pushPoints(pts).circle(S.BODY_PILOT_D / 2).extrude(inward * reach))
fp = [(a * S.TRUNK_FLOOR_SCREW_X / 2, b * S.TRUNK_FLOOR_SCREW_Y / 2) for a in (1, -1) for b in (1, -1)]
bottom = bottom.cut(cq.Workplane("XY", origin=(0, 0, BOTTOM_Z - 1)).pushPoints(fp).circle(FLOOR_SCREW_D / 2).extrude(TRUNK_SEAT_Z - BOTTOM_Z + 2))
seat = TRUNK_SEAT_Z - FLOOR_SCREW_HEAD_SEAT
bottom = bottom.cut(cq.Workplane("XY", origin=(0, 0, BOTTOM_Z - 1)).pushPoints(fp).circle(FLOOR_SCREW_HEAD_D / 2).extrude(seat - BOTTOM_Z + 1))

result = bottom
