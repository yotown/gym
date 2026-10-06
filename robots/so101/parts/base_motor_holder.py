"""SO-101 base motor holder, written from its STEP: the cage the shoulder-pan servo stands in.

A tapered portal frame seen from the front (the x-z plane), 20 deep along y, around the STS3215
that stands upright in it (its output shaft up, along z); behind the frame a low tray. Underneath,
a dovetail slot along x takes the driver-board plate's tenon (slid in from +x). Frame: the vendor's
STEP (mm): x across, y front (38.1) to back (69.5), z up; symmetric about x = 0 but for the slot.
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # SO-101's shared values (../shared.py): its servo, its screws
SERVO, SERVO_SCREW = S.SERVO, S.SERVO_SCREW

# -- interfaces: fixed -----------------------------------------------------------------------------
SERVO_X, SERVO_Z = 0.099, 32.7             # the STS3215's origin (x, z); its length along z
SLOT_Y = 49.75                             # the plate's dovetail slot, along x, open at +x
SLOT_NECK, SLOT_HEAD = 16.1, 18.3          # its widths at the underside and inside (the tenon: 15.9 / 18.1)
SLOT_NECK_H, SLOT_FLARE_H, SLOT_HEAD_H = 1.2, 1.38, 1.2   # measured
SLOT_END_X = -8.6                          # its closed end
PIN_Y, PIN_Z = 48.1, -4.5                  # the cross screw through the side walls
PIN_D, PIN_HEAD_D, PIN_HEAD_DEPTH = 2.0, 3.6, 2.0
BOTTOM_Z, FLOOR = -20.8, 4.8
FRAME_FROM_Y = 38.1
HALF_WIDTH = 22.35                         # the feet, straight up to the shoulder ...
SHOULDER_Z = 7.0
TAPER_DEG = 7.43                           # measured: ... then tapering to the top
WALL = 4.0                                 # the tapered sides and the top bar, over the servo
BAY_HALF_WIDTH, BAY_TOP_Z, BAY_R = 17.45, 18.5, 2.9   # the open bay under the servo

# -- body: free ------------------------------------------------------------------------------------
SERVO_Y = 46.1                             # its origin along y: the envelope runs through the frame, so free here
FRAME_TO_Y, TRAY_TO_Y = 58.1, 69.5         # the frame's and the tray's back faces
TOP_R = 5.0
PAD_HALF_WIDTH = 14.35                     # the side pads beside the servo, above the bay
TRAY_WALL_TOP_Z = 11.4                     # the tray's walls slope from the shoulder to here
EDGE_R = 1.0                               # the edges broken, as the vendor's (R1 on most of them)
# a snap-in cable clip on the +x wall: a block with a channel along y and a mouth to push the cable in
CLIP_Y = (43.9, 54.45)                     # its depth  # measured
CLIP_Z = (13.0, 25.5)                      # its extent up the wall  # measured
CLIP_PROUD, CLIP_R = 3.6, 0.8              # its face parallel to the wall, this far out; its edges rounded
CHANNEL = (3.0, 5.4)                       # the cable channel: a slot this wide (x) and tall (z)  # measured
CHANNEL_AT = (22.0, 19.2)                  # (x, z) of its axis, along y  # measured
MOUTH = 2.0                                # the slot the cable is pushed in through

top_z = SERVO_Z + SERVO.half_length + WALL
top_half = HALF_WIDTH - (top_z - SHOULDER_Z) * math.tan(math.radians(TAPER_DEG))
floor_z = BOTTOM_Z + FLOOR
depth, tray_depth = FRAME_TO_Y - FRAME_FROM_Y, TRAY_TO_Y - FRAME_FROM_Y


def front(y_back):
    """A front-view sketch (x, z) on the plane y = y_back, extruded toward the front (-y)."""
    return cq.Workplane("XZ", origin=(0, y_back, 0))


def symmetric(half):
    return half + [(-x, z) for x, z in reversed(half)]


# the portal frame and the tray behind it
tower = symmetric([(HALF_WIDTH, BOTTOM_Z), (HALF_WIDTH, SHOULDER_Z), (top_half, top_z)])
body = front(FRAME_TO_Y).polyline(tower).close().extrude(depth)
body = body.edges("|Y and >Z").fillet(TOP_R)
tray = symmetric([(HALF_WIDTH, BOTTOM_Z), (HALF_WIDTH, SHOULDER_Z), (BAY_HALF_WIDTH, TRAY_WALL_TOP_Z)])
body = body.union(front(TRAY_TO_Y).polyline(tray).close().extrude(tray_depth))

# inside: the bay over the floor, then the frame's walls (WALL thick) down to the side pads
bay = (front(TRAY_TO_Y).center(0, (floor_z + BAY_TOP_Z) / 2).rect(2 * BAY_HALF_WIDTH, BAY_TOP_Z - floor_z)
       .extrude(tray_depth).edges("|Y and <Z").fillet(BAY_R))
inside = front(FRAME_TO_Y).polyline(tower).close().offset2D(-WALL).extrude(depth)
pads = front(FRAME_TO_Y).center(0, top_z).rect(2 * PAD_HALF_WIDTH, 2 * (top_z - BAY_TOP_Z)).extrude(depth)
body = body.cut(bay).cut(inside.intersect(pads))

# the edges broken: the front and back rims (the uprights with them), then the edges running
# across (in this order: all at once, or the uprights first, the kernel cannot round them)
body = body.faces("<Y").edges().fillet(EDGE_R)
body = body.faces(">Y").edges().fillet(EDGE_R)
body = body.edges("|X").fillet(EDGE_R)

# the cable clip: a block rooted in the +x wall, its face following the wall's taper; then the
# channel along it and the mouth out through its face
def wall_x(z):
    """The +x wall's outer face at height z, above the shoulder."""
    return HALF_WIDTH - (z - SHOULDER_Z) * math.tan(math.radians(TAPER_DEG))


root_x = HALF_WIDTH - WALL / 2
clip = [(root_x, CLIP_Z[0]), (wall_x(CLIP_Z[0]) + CLIP_PROUD, CLIP_Z[0]),
        (wall_x(CLIP_Z[1]) + CLIP_PROUD, CLIP_Z[1]), (root_x, CLIP_Z[1])]
clip = (front(CLIP_Y[1]).polyline(clip).close().extrude(CLIP_Y[1] - CLIP_Y[0])
        .faces(">X").edges("|Y").fillet(CLIP_R))
body = body.union(clip)
cx, cz = CHANNEL_AT
body = body.cut(front(CLIP_Y[1]).center(cx, cz).slot2D(CHANNEL[1], CHANNEL[0], angle=90).extrude(CLIP_Y[1] - CLIP_Y[0]))
body = body.cut(front(CLIP_Y[1]).center((cx + HALF_WIDTH + CLIP_PROUD) / 2, cz)
                .rect(HALF_WIDTH + CLIP_PROUD - cx, MOUTH).extrude(CLIP_Y[1] - CLIP_Y[0]))

# -- interfaces, cut last -------------------------------------------------------------------------
# the servo's envelope
body = body.cut(front(SERVO_Y + SERVO.axis_span[1]).center(SERVO_X, SERVO_Z)
                .rect(SERVO.width, 2 * SERVO.half_length).extrude(SERVO.axis_span[1] - SERVO.axis_span[0]))
# the plate's dovetail slot under the floor, from its closed end out through the +x side
n, h = SLOT_NECK / 2, SLOT_HEAD / 2
dovetail = symmetric([(n, 0), (n, SLOT_NECK_H), (h, SLOT_NECK_H + SLOT_FLARE_H), (h, SLOT_NECK_H + SLOT_FLARE_H + SLOT_HEAD_H)])
body = body.cut(cq.Workplane("YZ", origin=(SLOT_END_X, SLOT_Y, BOTTOM_Z)).polyline(dovetail).close()
                .extrude(HALF_WIDTH - SLOT_END_X + 1))
# the cross screw through both side walls, its heads sunk from outside
pin = cq.Workplane("YZ", origin=(-HALF_WIDTH, PIN_Y, PIN_Z))
body = body.cut(pin.circle(PIN_D / 2).extrude(2 * HALF_WIDTH))
body = body.cut(pin.circle(PIN_HEAD_D / 2).extrude(PIN_HEAD_DEPTH))
body = body.cut(pin.workplane(offset=2 * HALF_WIDTH - PIN_HEAD_DEPTH).circle(PIN_HEAD_D / 2).extrude(PIN_HEAD_DEPTH))

result = body
