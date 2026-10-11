"""Flamingo wing mount: the wing servo's cradle on the body's side.

A plate on each of the case's two faces, from past the wing's yoke to the case's far end, each held by the
case's two far screws (as the Duck's sheets hold a servo) and recessed for the face's raised middle; a base
across the far end, screwed through the body's side wall by two M3s whose heads sink flush under the case
(nuts inside the shell), with a window for the servo's cable.

Frame: the servo's own (shared.py): x = back, y = across, z = into; origin on the axis at the horn face.
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)
F = S.F

# -- interfaces -- fixed ----------------------------------------------------------------------------
FAR = S.FAR                             # the base's inner face
HORN_FACE, IDLER_FACE = F.horn_side, F.idler_side   # the case's faces: their levels, screws, raised middles
SCREW = S.CLEARANCE[HORN_FACE.thread]
SCREW_GRIP = 2.0                           # under each M2's head, to the case's face
FOOT_BACK = 19.0                           # the case's screws further back than this are the plates'
BASE_SCREW = S.CLEARANCE["M3"]
BASE_HEAD_DEEP = 3.2

# -- body: free -------------------------------------------------------------------------------------
T, B = S.PLATE_T, S.BASE_T
FROM = 17.0                                # the plates start this far back: clear of the yoke (r 11.5) by 5.5
HALF_W = F.case_width / 2 + 2.5            # across: the case and a wall each side
BOSS_FIT = 0.2
z0, z1 = HORN_FACE.level - T, IDLER_FACE.level + T


def box(x0, x1, y0, y1, za, zb):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, zb - za, centered=False).translate((x0, y0, za))


mount = (box(FROM, FAR, -HALF_W, HALF_W, z0, HORN_FACE.level)
         .union(box(FROM, FAR, -HALF_W, HALF_W, IDLER_FACE.level, z1))
         .union(box(FAR, FAR + B, -HALF_W, HALF_W, z0, z1)))
# each face's raised middle, in its plate's inner face, from the plate's start to where it ends
for face, inner, d in ((HORN_FACE, HORN_FACE.level, -1), (IDLER_FACE, IDLER_FACE.level, 1)):
    if face.boss:
        w, back, deep = face.boss
        mount = mount.cut(box(FROM - 1, back, -(w / 2 + BOSS_FIT), w / 2 + BOSS_FIT,
                              *sorted((inner, inner + d * (deep + BOSS_FIT)))))
# the case's far screws through each plate, heads sunk to leave SCREW_GRIP under them
for face, inner, d in ((HORN_FACE, HORN_FACE.level, -1), (IDLER_FACE, IDLER_FACE.level, 1)):
    pts = [(back, across) for back, across in face.screws if back > FOOT_BACK]
    wp = cq.Workplane(cq.Plane(origin=(0, 0, inner), xDir=(1, 0, 0), normal=(0, 0, d)))
    mount = mount.cut(wp.pushPoints(pts).circle(SCREW.hole_d / 2).extrude(T + 1))
    mount = mount.cut(wp.workplane(offset=SCREW_GRIP).pushPoints(pts).circle(SCREW.head_d / 2).extrude(T))
# the base: two M3s out through the wall, heads from the case's side; the cable's window
base = cq.Workplane(cq.Plane(origin=(FAR, 0, 0), xDir=(0, 1, 0), normal=(1, 0, 0)))
pts = [(across, into) for into, across in S.BASE_SCREWS]
mount = mount.cut(base.pushPoints(pts).circle(BASE_SCREW.hole_d / 2).extrude(B + 1))
mount = mount.cut(base.pushPoints(pts).circle(BASE_SCREW.head_d / 2).extrude(BASE_HEAD_DEEP))
c0, c1, ch = S.CABLE_WINDOW
mount = mount.cut(box(FAR - 1, FAR + B + 1, -ch, ch, c0, c1))
result = mount
