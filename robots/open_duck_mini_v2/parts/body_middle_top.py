"""Open Duck Mini v2 body middle (the top half), written from its STEP: interfaces exact, the body simple.

A shell of the body's section (as body_front's) above the split line, open on top in a window; near each
end a frame inside it, and four bosses taking the front and back plates' screws.

Frame: the vendor's (mm): the shell runs along x from the back plate's joint to the front plate's; the
section in (y, z).
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)
INSERT = S.INSERT

# -- interfaces -- fixed ----------------------------------------------------------------------------
SCREW_YZ = [(45.0, 17.408), (29.408, 33.0)]   # the plates' screws into the bosses, each and its mirror in y

# -- body: free -------------------------------------------------------------------------------------
WALL = 3.0
WINDOW_HALF_W = 25.0                       # in the top (y),
WINDOW_X = (-55.0, 45.0)                   # from-to
BOSS_D = 8.0


def section(inset):
    """The body's section moved in by inset."""
    wp = cq.Workplane("YZ", origin=(S.BODY_BACK_JOINT_X, 0, 0)).polyline(S.BODY_SECTION).close()
    return wp.offset2D(-inset, "intersection") if inset else wp


def prism(inset, x0, x1):
    """The section moved in by inset, between x0 and x1, above the split."""
    above = cq.Workplane("XY", origin=(0, 0, S.BODY_SPLIT_Z)).center((x0 + x1) / 2, 0).rect(x1 - x0 + 2, 200).extrude(100)
    return section(inset).extrude(S.BODY_FRONT_JOINT_X - S.BODY_BACK_JOINT_X).intersect(above).intersect(
        cq.Workplane("XY", origin=(0, 0, -200)).center((x0 + x1) / 2, 0).rect(x1 - x0, 200).extrude(400))


shell = prism(0, S.BODY_BACK_JOINT_X, S.BODY_FRONT_JOINT_X).cut(prism(WALL, S.BODY_BACK_JOINT_X - 1, S.BODY_FRONT_JOINT_X + 1))
w0, w1 = WINDOW_X
shell = shell.cut(cq.Workplane("XY", origin=(0, 0, S.BODY_SPLIT_Z)).center((w0 + w1) / 2, 0).rect(w1 - w0, 2 * WINDOW_HALF_W).extrude(100))
frames = [(S.BODY_BACK_JOINT_X + S.BODY_FRAME_IN, S.BODY_BACK_JOINT_X + S.BODY_FRAME_IN + S.BODY_FRAME_T), (S.BODY_FRONT_JOINT_X - S.BODY_FRAME_IN - S.BODY_FRAME_T, S.BODY_FRONT_JOINT_X - S.BODY_FRAME_IN)]
for x0, x1 in frames:
    shell = shell.union(prism(WALL - 0.01, x0, x1).cut(prism(WALL + S.BODY_FRAME_W, x0 - 1, x1 + 1)))

# -- interfaces, cut last -------------------------------------------------------------------------
pts = [(s * y, z) for y, z in SCREW_YZ for s in (1, -1)]
for end, inward in ((S.BODY_BACK_JOINT_X, 1), (S.BODY_FRONT_JOINT_X, -1)):
    reach = S.BODY_FRAME_IN + S.BODY_FRAME_T                 # each boss runs from the joint to the frame's far side
    wp = cq.Workplane("YZ", origin=(end, 0, 0))
    shell = shell.union(wp.pushPoints(pts).circle(BOSS_D / 2).extrude(inward * reach))
    shell = shell.cut(wp.pushPoints(pts).circle(INSERT.hole_d / 2).extrude(inward * INSERT.depth))
    shell = shell.cut(wp.pushPoints(pts).circle(S.BODY_PILOT_D / 2).extrude(inward * reach))

result = shell
