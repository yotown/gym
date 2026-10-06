"""Open Duck Mini v2: what its parts share. A part reads it with `shared(__file__)`.

Each value here is an interface two or more parts fit: change it here and every part that uses it
follows. A value only one part uses stays in that part.
"""

from yotown.gym.interfaces import Screw
from yotown.gym.vendors.fasteners import HeatSetInsert
from yotown.gym.vendors.feetech import STS3215

SERVO = STS3215()                          # every joint
HORN = SERVO.horn.rotated(-45.0)           # the Duck's parts put the horn's four holes on their frame's axes

# the screws and inserts, as the printed parts take them
HORN_SCREW = Screw(hole_d=3.2, head_d=6.5)  # into the horn (the head's parts counterbore their heads 5.5)
SERVO_SCREW_D = 2.5                        # into the servo's tabs (their heads differ by part)
INSERT = HeatSetInsert(hole_d=4.0, depth=5.8, thread="M3")   # in the body's shells, the trunk and the feet

# -- mates: values two parts in one frame both fit -------------------------------------------------
# the body's shells
BODY_SCREW_YZ = [(45.0, 17.408), (45.0, -22.313), (45.0, -62.033), (29.408, 33.0)]   # the screws joining the middle to the back and the front (y, z), each and its mirror in y
BODY_SPLIT_Z = -13.775                     # where the middle's bottom half meets its top half
BODY_BACK_JOINT_X = -95.0                  # the middle's joint with the back
BODY_FRONT_JOINT_X = 55.0                  # the middle's joint with the front plate
BODY_PILOT_D = 3.0                         # the pilot past each joint screw's insert
TRUNK_FLOOR_SCREW_X = 20.0                 # the middle's floor screws into the trunk: on a rectangle this long (x)
TRUNK_FLOOR_SCREW_Y = 20.0                 # and this wide (y)

# the body's shape, shared by its shells: free to change, but together
BODY_SECTION = [(55.0, 21.55), (33.55, 43.0), (-33.55, 43.0), (-55.0, 21.55), (-55.0, -64.25), (-38.33, -100.0),
                (38.33, -100.0), (55.0, -64.25)]   # the cross-section (y, z) of the front and the middle (the back ends higher)
BODY_FRAME_T = 3.0                         # the middle's inner frames near each joint: this thick (x),
BODY_FRAME_IN = 7.0                        # this far in from the joint,
BODY_FRAME_W = 3.0                         # this wide in from the wall

# the face: the eyes and the bulb, on the head's front (no model of these parts: their fits are declared)
FACE_CENTRE_Z = 139.41                     # the eye holes' centre height
FACE_SCREW_SQUARE = 25.0                   # the screws into the head's front, on a square about each eye
EYE_BACK_X = 120.0                         # the eyes' back face, on the head's front
EYE_LENS_D = 25.0                          # the lens, seated from the back,
EYE_OPENING_D = 29.6                       # then the opening to the front

# the flash light and its reflector (no model of these parts)
FLASH_AXIS_Y, FLASH_AXIS_Z = 99.093, 144.54    # the light's axis, along x

# the speaker's stand and interface (no model of these parts)
SPEAKER_TURN = -15.705                     # their frame, turned about z from the vendor's  # measured
SPEAKER_TILT_DEG = 13.67                   # the stand's tilted leg, back from the vertical  # measured

# the head and the neck
HEAD_RIM_Z = 109.71                        # the head's rim, on the bottom sheet
NECK_YAW_X, NECK_YAW_Y = 20.0, 0.0         # the head yaw servo's axis, along z

# the hips and the legs
TRUNK_HIP_Y = 35.0                         # the hip yaw axes, each side of the trunk
HIP_YAW_X, HIP_YAW_Y = 0.0, 35.0           # the hip yaw axis in the roll motor mounts' frame, vertical
LEG_ROD_PITCH = 16.0                       # the knee's rods: their pitch on the sheets and the spacer

# the feet
FOOT_SOLE_Z = -253.625                     # the foot's sole
FOOT_SCREW_X = [-26.762, 13.238]           # the pads' screws, up from below: along x,
FOOT_SCREW_Y = 90.0                        # and y
