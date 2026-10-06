"""Open Duck Mini v2 hip roll-to-pitch link (left), written from its STEP: interfaces exact, the body simple.
right_roll_to_pitch is this part mirrored across the robot's middle (y = 0).

A fork on the hip roll servo -- two arms, round about the roll axis, each with the servo's horn mount (the
horn's bore and four screws counterbored from outside), tapering to a crossbar -- and behind it a
bracket for the hip pitch servo: a top plate, a side wall (the outer arm, carried on), two end plates
cut back on a diagonal, and a lip under the servo. The pitch servo screws into both end plates; the
screws at the front are reached through long bores in the outer arm.

Frame: the vendor's (mm). The roll axis runs along x through ROLL (y, z); the link reaches along +y.
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)
HORN, HORN_SCREW = S.HORN, S.HORN_SCREW

# -- interfaces -- fixed ----------------------------------------------------------------------------
# the hip roll servo, between the arms
ROLL_Y, ROLL_Z = 35.0, -65.0               # its axis, along x
ARM_INNER_X = (-17.8, 19.05)               # the arms' inner faces: its horns sit on them
HORN_BORE_D = 7.6                          # each horn's hub, into the arm
HORN_BORE_DEEP = 1.5
HORN_THROUGH_D = 7.0
HORN_SCREW_HEAD_SEAT = 3.0                 # out from the horn's seat
# the hip pitch servo, in the bracket
SERVO_TOP_Z = -52.44                       # under the top plate
SERVO_BOTTOM_Z = -77.36                    # on the lip
SERVO_BACK_Y = 106.1                       # against the back plate
SERVO_FRONT_Y = 73.9                       # against the front plate,
FLANGE_POCKET_Y = 72.1                     # its flange in a pocket in it, to here,
FLANGE_POCKET_X = (1.44, 13.69)            # x,
FLANGE_POCKET_Z = (-74.24, -55.76)         # z
BACK_SCREW_XZ = [(12.94, -54.75), (12.94, -75.25), (-7.76, -54.75)]   # through the back plate
BACK_SCREW_D = 2.5
BACK_SCREW_HEAD_D = 4.0
BACK_SCREW_HEAD_SEAT = 2.0                 # out from the servo's back
FRONT_SCREW_X = 16.69                      # into the front plate,
FRONT_SCREW_Z = (-54.75, -75.25)
FRONT_SCREW_D = 2.5
FRONT_SCREW_DEEP = 2.9                     # from the servo's front
FRONT_ACCESS_D = 5.0                       # reached through a bore in the outer arm
PITCH_X, PITCH_Z = -16.053, -64.993        # the hip pitch axis (along y): the back plate is cleared round it  # measured

# -- body: free -------------------------------------------------------------------------------------
FRONT_ACCESS_TO_Y = 29.38                  # the front screws' access bores, back to here
ARM_T = 5.0                                # each arm's thickness (x)
LOW_Z, HIGH_Z = -80.36, -49.64             # the link's height
ARM_R = 10.975                             # the arms' round end about the roll axis,  # measured
TAPER_DEG = 14.65                          # tapering out from it to the link's full height  # measured
BAR_Y = (62.37, 67.37)                     # the crossbar: from-to,
BAR_R = 5.0                                # its inner corners' round
TOP_PLATE_FROM_X = -10.51                  # the top plate, from x to the outer arm
FRONT_PLATE_FROM_X = 1.44                  # the front plate, from the crossbar to the servo's front, from x
BACK_PLATE_T = 4.0
BACK_PLATE_FROM_X = -10.51
DIAGONAL = (14.53, -80.36)                 # both end plates are cut back on 45 deg through this (x, z)
LIP_FROM_X = 12.53                         # under the servo, along the outer arm
CUTOUT_R = 11.4035                         # the back plate cleared round the hip pitch joint  # measured
EDGE_CHAMFER = 1.0                         # the arms' outer faces' long edges
BAR_END_R = 5.0                            # the crossbar's outer end, round about z on the outer arm's side

lo, hi = LOW_Z, HIGH_Z
ry, rz = ROLL_Y, ROLL_Z
xin_l, xin_r = ARM_INNER_X
x_left, x_right = xin_l - ARM_T, xin_r + ARM_T
end_y = SERVO_BACK_Y + BACK_PLATE_T
b0, b1 = BAR_Y
FRONT_PLATE = (b1, SERVO_FRONT_Y, FRONT_PLATE_FROM_X)
BACK_PLATE = (SERVO_BACK_Y, end_y, BACK_PLATE_FROM_X)
front_face = SERVO_FRONT_Y - FRONT_SCREW_DEEP   # the front screws' holes end here, the access bores start
k = math.tan(math.radians(TAPER_DEG))
full_from = ry + (hi - rz - ARM_R / math.cos(math.radians(TAPER_DEG))) / k   # where the taper reaches full height


def arm(x0, x1, x_out):
    """An arm (x0 to x1): round about the roll axis, tapering out to full height, on to the crossbar; its
    outer face's long edges chamfered."""
    t = math.radians(TAPER_DEG)
    tan_pts = [(ry + ARM_R * math.sin(t), rz + s * ARM_R * math.cos(t)) for s in (1, -1)]
    prof = (cq.Workplane("YZ", origin=(x0, 0, 0)).moveTo(*tan_pts[1]).threePointArc((ry - ARM_R, rz), tan_pts[0])
            .lineTo(full_from, hi).lineTo(b0, hi).lineTo(b0, lo).lineTo(full_from, lo).close())
    return prof.extrude(x1 - x0).edges("|Y").edges(cq.selectors.NearestToPointSelector((x_out, (full_from + b0) / 2, hi))).chamfer(EDGE_CHAMFER) \
        .edges("|Y").edges(cq.selectors.NearestToPointSelector((x_out, (full_from + b0) / 2, lo))).chamfer(EDGE_CHAMFER)


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY", origin=(0, 0, z0)).center((x0 + x1) / 2, (y0 + y1) / 2).rect(x1 - x0, y1 - y0).extrude(z1 - z0)


link = arm(x_left, xin_l, x_left).union(arm(xin_r, x_right, x_right))
link = link.union(box(xin_r, x_right, b1, end_y, lo, hi))       # the outer arm carried on, the bracket's side
link = link.union(box(x_left, x_right, b0, b1, lo, hi))
link = link.union(box(TOP_PLATE_FROM_X, x_right, front_face, end_y, SERVO_TOP_Z, hi))
dx, dz = DIAGONAL
for y0, y1, x0 in (FRONT_PLATE, BACK_PLATE):
    plate = box(x0, x_right, y0, y1, lo, hi)
    # cut back below the 45 deg diagonal through DIAGONAL
    keep = cq.Workplane("XZ", origin=(0, y1 + 1, 0)).polyline([(dx, lo), (x0 - 1, lo + dx - x0 + 1), (x0 - 1, hi + 1), (x_right + 1, hi + 1), (x_right + 1, lo)]) \
        .close().extrude(y1 - y0 + 2)
    link = link.union(plate.intersect(keep))
(fx0, fx1), (fz0, fz1) = FLANGE_POCKET_X, FLANGE_POCKET_Z
link = link.cut(box(fx0, fx1, FLANGE_POCKET_Y, SERVO_FRONT_Y + 1, fz0, fz1))
link = link.union(box(LIP_FROM_X, xin_r, SERVO_FRONT_Y, SERVO_BACK_Y, lo, SERVO_BOTTOM_Z))
link = link.cut(cq.Workplane("XZ", origin=(0, end_y + 1, 0)).center(PITCH_X, PITCH_Z).circle(CUTOUT_R).extrude(BACK_PLATE_T + 2))
corner = box(x_left - 1, x_left + BAR_END_R, b1 - BAR_END_R, b1 + 1, lo - 1, hi + 1)
link = link.cut(corner.cut(cq.Workplane("XY", origin=(0, 0, lo - 1)).center(x_left + BAR_END_R, b1 - BAR_END_R).circle(BAR_END_R).extrude(hi - lo + 2)))
# the crossbar's inner corners
link = link.edges(cq.selectors.BoxSelector((xin_l - 0.1, b0 - 0.1, lo - 1), (xin_l + 0.1, b0 + 0.1, hi + 1))).fillet(BAR_R) \
    .edges(cq.selectors.BoxSelector((xin_r - 0.1, b0 - 0.1, lo - 1), (xin_r + 0.1, b0 + 0.1, hi + 1))).fillet(BAR_R)

# -- interfaces, cut last -------------------------------------------------------------------------
pts = HORN.points(at=(ry, rz))
for x_in, x_out in ((xin_l, x_left), (xin_r, x_right)):
    s = 1 if x_out > x_in else -1          # outwards
    through = cq.Workplane("YZ", origin=(min(x_in, x_out) - 1, 0, 0))
    link = link.cut(through.center(ry, rz).circle(HORN_THROUGH_D / 2).extrude(ARM_T + 2)).cut(through.pushPoints(pts).circle(HORN_SCREW.hole_d / 2).extrude(ARM_T + 2))
    link = link.cut(cq.Workplane("YZ", origin=(x_in, 0, 0)).center(ry, rz).circle(HORN_BORE_D / 2).extrude(s * HORN_BORE_DEEP))
    link = link.cut(cq.Workplane("YZ", origin=(x_in + s * HORN_SCREW_HEAD_SEAT, 0, 0)).pushPoints(pts).circle(HORN_SCREW.head_d / 2).extrude(s * (ARM_T + 1)))
back = cq.Workplane("XZ", origin=(0, end_y + 1, 0))   # its normal -y: into the plate
seat = SERVO_BACK_Y + BACK_SCREW_HEAD_SEAT
link = link.cut(back.pushPoints(BACK_SCREW_XZ).circle(BACK_SCREW_HEAD_D / 2).extrude(end_y + 1 - seat))
link = link.cut(back.pushPoints(BACK_SCREW_XZ).circle(BACK_SCREW_D / 2).extrude(end_y + 1 - SERVO_BACK_Y))
pts = [(FRONT_SCREW_X, z) for z in FRONT_SCREW_Z]
link = link.cut(cq.Workplane("XZ", origin=(0, SERVO_FRONT_Y, 0)).pushPoints(pts).circle(FRONT_SCREW_D / 2).extrude(FRONT_SCREW_DEEP))
link = link.cut(cq.Workplane("XZ", origin=(0, front_face, 0)).pushPoints(pts).circle(FRONT_ACCESS_D / 2).extrude(front_face - FRONT_ACCESS_TO_Y))

result = link
