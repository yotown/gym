"""Open Duck Mini v2 bulb mount, written from its STEP: interfaces exact, the body simple.

A round plate on the head's face with an ear at each of its four screws, each ear joined to the round by
two R2.5 scallops (as the left eye's). In its back a pocket
for the bulb's board, with four holes for its parts; through the middle a slot and a hole for the bulb.

Frame: the vendor's (mm): the plate's back face is x = BACK, its front x = FRONT; it lies in (y, z).
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
# this part is not in the model: what it fits is declared
CENTRE_Y = -40.0                           # on the head's eye hole; not in the model: this part
FRONT_X = 117.0                            # against the head's front wall, inside; not in the model: this part
SCREW_D = 2.7
BOARD_W, BOARD_H = 15.0, 12.0              # the LED board's pocket in the back; not in the model: the LED board
BOARD_DEEP = 1.2                           # not in the model: the LED board
BOARD_FROM = 0.3                           # from x (past the back's chamfer); not in the model: the LED board
BOARD_HOLE_W, BOARD_HOLE_H = 10.0, 7.0     # four in the pocket's floor, on a rectangle; not in the model: the LED board
BOARD_HOLE_D = 5.0                         # not in the model: the LED board
BULB_SLOT_W, BULB_SLOT_H = 7.25, 3.62      # the LED through the middle: a slot; not in the model: the LED  # measured
BULB_HOLE_D = 8.1                          # and a hole; not in the model: the LED  # measured

# -- body: free -------------------------------------------------------------------------------------
PLATE_T = 2.0
ROUND_D, EAR_R = 35.0, 2.75                # the plate: a round, an ear about each screw
SCALLOPS = (2.5, 20.0, 14.4)               # r, their centres' distance from the middle, either side of each diagonal (deg)  # measured
BACK, FRONT = FRONT_X - PLATE_T, FRONT_X

cy, cz = CENTRE_Y, S.FACE_CENTRE_Z
side, d = S.FACE_SCREW_SQUARE, SCREW_D
r, dist, off = SCALLOPS
plane = cq.Workplane("YZ", origin=(BACK, 0, 0))
plate = plane.center(cy, cz).circle(ROUND_D / 2).extrude(FRONT - BACK)
for k in range(4):                         # each ear: its disc, and a wedge from the middle out to it, trimmed by the scallops
    a = math.radians(45 + 90 * k)
    sx, sz = cy + side / 2 * math.sqrt(2) * math.cos(a), cz + side / 2 * math.sqrt(2) * math.sin(a)
    rim = [(cy + ROUND_D / 2 * math.cos(a + s * math.radians(2 * off)), cz + ROUND_D / 2 * math.sin(a + s * math.radians(2 * off))) for s in (-1, 1)]
    plate = plate.union(plane.center(sx, sz).circle(EAR_R).extrude(FRONT - BACK))
    plate = plate.union(plane.polyline([(cy, cz), rim[0], (sx, sz), rim[1]]).close().extrude(FRONT - BACK))
pts = [(cy + dist * math.cos(math.radians(45 + 90 * k + s * off)), cz + dist * math.sin(math.radians(45 + 90 * k + s * off)))
       for k in range(4) for s in (1, -1)]
bulb = plate.cut(cq.Workplane("YZ", origin=(BACK - 1, 0, 0)).pushPoints(pts).circle(r).extrude(FRONT - BACK + 2))

(bw, bh), bdeep, bfrom = (BOARD_W, BOARD_H), BOARD_DEEP, BOARD_FROM
bulb = bulb.cut(cq.Workplane("YZ", origin=(BACK - 1, 0, 0)).center(cy, cz).rect(bw, bh).extrude(1 + bfrom + bdeep))
(hw, hh), hd = (BOARD_HOLE_W, BOARD_HOLE_H), BOARD_HOLE_D
bulb = bulb.cut(cq.Workplane("YZ", origin=(BACK - 1, 0, 0)).pushPoints([(cy + sy * hw / 2, cz + sz * hh / 2) for sy in (1, -1) for sz in (1, -1)])
                .circle(hd / 2).extrude(1 + bfrom + bdeep))
(sw, sh), hole = (BULB_SLOT_W, BULB_SLOT_H), BULB_HOLE_D
bulb = bulb.cut(cq.Workplane("YZ", origin=(BACK - 1, 0, 0)).center(cy, cz).rect(sw, sh).extrude(FRONT - BACK + 2))
bulb = bulb.cut(cq.Workplane("YZ", origin=(BACK + bfrom + bdeep, 0, 0)).center(cy, cz).circle(hole / 2).extrude(FRONT - BACK))
corners = [(cy + sy * side / 2, cz + sz * side / 2) for sy in (1, -1) for sz in (1, -1)]
bulb = bulb.cut(cq.Workplane("YZ", origin=(BACK - 1, 0, 0)).pushPoints(corners).circle(d / 2).extrude(FRONT - BACK + 2))

result = bulb
