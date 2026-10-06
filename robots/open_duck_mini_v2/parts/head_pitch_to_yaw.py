"""Open Duck Mini v2 head pitch-to-yaw yoke, written from its STEP: interfaces exact, the body simple.

Below, a fork on the head pitch servo: two arms, each round about the pitch axis and drafted up to a
bottom plate, each with a horn mount (the horn's bore, four screws counterbored from outside, a slot on
the inner face from the bore to the round end). Above, a C-frame round the head yaw servo: the bottom
plate and a top plate, both with the yaw horn's pattern on the yaw axis (counterbored from outside, a
slot on the inner face out to the free end), joined by a wall at the back; the wall's corners rounded.

Frame: the vendor's (mm). The pitch axis runs along y through PITCH (x, z); the yaw axis along z
through YAW (x, y).
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)
HORN, HORN_SCREW = S.HORN, S.HORN_SCREW

# -- interfaces -- fixed ----------------------------------------------------------------------------
PITCH_X, PITCH_Z = 20.0, 91.11             # the head pitch servo's axis, along y
ARM_INNER_Y = (-17.85, 19.05)              # the fork's arms' inner faces: the pitch servo's horns sit on them
PLATE_INNER_Z = (111.21, 148.11)           # the yaw servo between the plates: its horns sit on them (bottom, top)
HORN_BORE_D = 7.0                          # every horn: its bore,
HORN_SCREW_HEAD_D = 5.5
HORN_SCREW_HEAD_SEAT_ARM = 2.0             # out from the horn's seat, in an arm
HORN_SCREW_HEAD_SEAT_BOTTOM = 2.1          # in the bottom plate  # measured
HORN_SCREW_HEAD_SEAT_TOP = 2.0             # in the top plate

# -- body: free -------------------------------------------------------------------------------------
ARM_T = 4.0                                # each arm's thickness (y)
PLATE_T = (4.1, 4.0)                       # the plates' thickness (bottom, top)
ARM_R = 11.0                               # the arms' round end,
ARM_DRAFT_DEG = 2.96                       # their sides drafted in from it up to the plate  # measured
WALL_X = (-1.0, 3.0)                       # the C-frame's back wall: x from-to,
WALL_HALF_W = 11.0                         # half its width (y)
PLATE_X = (0.0, 29.975)                    # the plates (x): from the wall, out to a flat across the top plate's round end  # measured
TOP_HALF = 11.0                            # the top plate's half width (y); its end round about the yaw axis
CORNER_R = 3.0
PLATE_BACK_R = 9.0                         # the bottom plate's back corners (about z)  # measured
RELIEF_W = 7.0                             # each horn's relief: a slot from its bore on the inner face,
RELIEF_DEEP = 1.0                          # this deep

ARMS = [(ARM_INNER_Y[0] - ARM_T, ARM_INNER_Y[0]), (ARM_INNER_Y[1] + ARM_T, ARM_INNER_Y[1])]   # (outer, inner) each
PLATES = ((PLATE_INNER_Z[0] - PLATE_T[0], PLATE_INNER_Z[0]), (PLATE_INNER_Z[1], PLATE_INNER_Z[1] + PLATE_T[1]))


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY", origin=(0, 0, z0)).center((x0 + x1) / 2, (y0 + y1) / 2).rect(x1 - x0, y1 - y0).extrude(z1 - z0)


px, pz = PITCH_X, PITCH_Z
yx, yy = S.NECK_YAW_X, S.NECK_YAW_Y
(b0, b1), (t0, t1) = PLATES
# the fork's arms: round about the pitch axis, drafted up to the bottom plate's top
k = math.tan(math.radians(ARM_DRAFT_DEG))
side = [(px - ARM_R, pz), (px + ARM_R, pz), (px + ARM_R - k * (b1 - pz), b1), (px - ARM_R + k * (b1 - pz), b1)]
yoke = None
for y0, y1 in ARMS:
    lo, hi = min(y0, y1), max(y0, y1)
    arm = cq.Workplane("XZ", origin=(0, hi, 0)).polyline(side).close().extrude(hi - lo) \
        .union(cq.Workplane("XZ", origin=(0, hi, 0)).center(px, pz).circle(ARM_R).extrude(hi - lo))
    yoke = arm if yoke is None else yoke.union(arm)
o0, o1 = ARMS[0][0], ARMS[1][0]
x0, x1 = PLATE_X
(wx0, wx1), wh = WALL_X, WALL_HALF_W
plate = box(x0, px + ARM_R - k * (b1 - pz), o0 + 1, o1 - 1, b0, b1)        # the bottom plate, across the arms (1 inside their outer faces), its back corners round
plate = plate.edges("|Z").edges(cq.selectors.BoxSelector((x0 - 0.1, o0, b0 - 1), (x0 + 0.1, o1, b1 + 1))).fillet(PLATE_BACK_R)
yoke = yoke.union(plate)
yoke = yoke.union(box(wx0, wx1, yy - wh, yy + wh, b0, t1))                 # the wall
yoke = yoke.union(box(x0, yx, yy - TOP_HALF, yy + TOP_HALF, t0, t1)
                  .union(cq.Workplane("XY", origin=(0, 0, t0)).center(yx, yy).circle(TOP_HALF).extrude(t1 - t0))
                  .intersect(box(x0, x1, yy - TOP_HALF, yy + TOP_HALF, t0, t1)))   # the top plate, round about the yaw axis, flat at its end
yoke = yoke.edges(cq.selectors.BoxSelector((wx1 - 0.1, yy - wh, b1 - 0.1), (wx1 + 0.1, yy + wh, b1 + 0.1))).fillet(CORNER_R)
yoke = yoke.edges(cq.selectors.BoxSelector((wx1 - 0.1, yy - wh, t0 - 0.1), (wx1 + 0.1, yy + wh, t0 + 0.1))).fillet(CORNER_R)

# -- interfaces, cut last -------------------------------------------------------------------------
on_circle = lambda cx, cy: HORN.points(at=(cx, cy))
# the pitch horns, in each arm (xz)
for y_out, y_in in ARMS:
    s = 1 if y_in > y_out else -1          # into the fork
    through = cq.Workplane("XZ", origin=(0, max(y_out, y_in) + 1, 0))
    yoke = yoke.cut(through.center(px, pz).circle(HORN_BORE_D / 2).extrude(ARM_T + 2))
    yoke = yoke.cut(through.pushPoints(on_circle(px, pz)).circle(HORN_SCREW.hole_d / 2).extrude(ARM_T + 2))
    seat = y_in - s * HORN_SCREW_HEAD_SEAT_ARM
    head = cq.Workplane("XZ", origin=(0, max(seat, y_out), 0))
    yoke = yoke.cut(head.pushPoints(on_circle(px, pz)).circle(HORN_SCREW_HEAD_D / 2).extrude(abs(seat - y_out)))
    relief = cq.Workplane("XZ", origin=(0, y_in + (0 if s > 0 else RELIEF_DEEP), 0)).center(px, pz - ARM_R).rect(RELIEF_W, 2 * ARM_R).extrude(RELIEF_DEEP)
    yoke = yoke.cut(relief)
# the yaw horns, in both plates (xy): counterbored from outside, a relief on the inner face out to the plate's end
x1 = PLATE_X[1]
for (z_out, z_in), head_seat in zip(((PLATES[0][0], PLATES[0][1]), (PLATES[1][1], PLATES[1][0])), (HORN_SCREW_HEAD_SEAT_BOTTOM, HORN_SCREW_HEAD_SEAT_TOP)):
    s = 1 if z_in > z_out else -1
    zl = min(z_out, z_in)
    yoke = yoke.cut(cq.Workplane("XY", origin=(0, 0, zl - 1)).center(yx, yy).circle(HORN_BORE_D / 2).extrude(abs(z_in - z_out) + 2))
    yoke = yoke.cut(cq.Workplane("XY", origin=(0, 0, zl - 1)).pushPoints(on_circle(yx, yy)).circle(HORN_SCREW.hole_d / 2).extrude(abs(z_in - z_out) + 2))
    seat = z_in - s * head_seat
    yoke = yoke.cut(cq.Workplane("XY", origin=(0, 0, min(seat, z_out))).pushPoints(on_circle(yx, yy)).circle(HORN_SCREW_HEAD_D / 2).extrude(abs(seat - z_out)))
    yoke = yoke.cut(cq.Workplane("XY", origin=(0, 0, z_in - RELIEF_DEEP if s > 0 else z_in)).center((yx + x1 + 2) / 2, yy).rect(x1 + 2 - yx, RELIEF_W).extrude(RELIEF_DEEP))

result = yoke
