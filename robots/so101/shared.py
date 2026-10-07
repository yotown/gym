"""SO-101: what its parts share. A part reads it with `shared(__file__)`.

Each value here is an interface two or more parts fit: change it here and every part that uses it
follows. A value only one part uses stays in that part.
"""

from yotown.gym.interfaces import Screw
from yotown.gym.vendors.feetech import STS3215
from yotown.gym.vendors.waveshare import BUS_SERVO_ADAPTER_A

SERVO = STS3215()                          # all six joints
DRIVER_BOARD = BUS_SERVO_ADAPTER_A         # the servo driver board, on waveshare_plate

# the screws, as the printed parts take them
SERVO_SCREW = Screw(hole_d=2.0, head_d=4.0, grip=2.2)   # into the servo's tabs; heads from outside
HORN_SCREW_HEAD_D = 5.4                    # the horn's screws' heads (their holes differ by part: clearance or tight)
IDLER_SCREW_D = 3.2                        # into the idler boss (PA3.0 self-tapping)
HORN_SEAT_D = 20.2                         # a seat round the horn disc (d19.2), with clearance
