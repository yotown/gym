"""Open Duck Mini v2 flash reflector interface, written from its STEP: interfaces exact, the body simple.

A short tapered tube on the flash's axis: in its back a pocket for the light's board (turned like the
board), a wall with the light's hole and a slot through it, then the reflector -- a cone opening to the
front -- and a bore for the lens.

Frame: the vendor's (mm): the axis runs along x through AXIS (y, z).
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
# this part is not in the model: what it fits is declared
BACK_X = 101.3                             # on the flash light module; not in the model: this part
BOARD_LONG, BOARD_ACROSS = 15.0, 12.0      # the light's board, in a pocket in the back; not in the model: the light's board
BOARD_TURN_DEG = 20.0                      # turned about x; not in the model: the light's board
BOARD_DEEP = 1.5                           # not in the model: the light's board
LIGHT_HOLE_D = 8.1                         # through the wall: a hole; not in the model: the LED  # measured
LIGHT_SLOT_LONG, LIGHT_SLOT_ACROSS = 7.25, 3.62   # and a slot, turned with the board; not in the model: the LED  # measured
LENS_D = 20.0                              # the lens's bore, at the reflector's mouth, to the front; not in the model: the lens  # measured

# -- body: free -------------------------------------------------------------------------------------
FRONT_X = 114.0
WALL_T = 1.0                               # between the board's pocket and the reflector  # measured
OUTSIDE_BACK_D, OUTSIDE_FRONT_D = 21.67, 23.0   # the tube's outside  # measured
REFLECTOR_FOOT_D = 13.0                    # the cone: d at its foot,  # measured
REFLECTOR_LONG = 8.0                       # long  # measured
BACK, FRONT = BACK_X, FRONT_X

ay, az = S.FLASH_AXIS_Y, S.FLASH_AXIS_Z
d0, d1 = OUTSIDE_BACK_D, OUTSIDE_FRONT_D
tube = cq.Workplane().add(cq.Solid.makeCone(d0 / 2, d1 / 2, FRONT - BACK, cq.Vector(BACK, ay, az), cq.Vector(1, 0, 0)))
(bl, bw), turn, bdeep = (BOARD_LONG, BOARD_ACROSS), BOARD_TURN_DEG, BOARD_DEEP
back = cq.Workplane("YZ", origin=(BACK - 1, 0, 0)).center(ay, az).transformed(rotate=(0, 0, turn))
tube = tube.cut(back.rect(bl, bw).extrude(1 + bdeep))
hole, (sl, sw), wall = LIGHT_HOLE_D, (LIGHT_SLOT_LONG, LIGHT_SLOT_ACROSS), WALL_T
tube = tube.cut(back.circle(hole / 2).extrude(1 + bdeep + wall + 0.01)).cut(back.rect(sl, sw).extrude(1 + bdeep + wall + 0.01))
foot, mouth, long_ = REFLECTOR_FOOT_D, LENS_D, REFLECTOR_LONG
cone_from = BACK + bdeep + wall
tube = tube.cut(cq.Workplane().add(cq.Solid.makeCone(foot / 2, mouth / 2, long_, cq.Vector(cone_from, ay, az), cq.Vector(1, 0, 0))))
tube = tube.cut(cq.Workplane("YZ", origin=(cone_from + long_ - 0.01, 0, 0)).center(ay, az).circle(mouth / 2).extrude(FRONT - cone_from - long_ + 1))

result = tube
