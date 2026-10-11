"""The Flamingo: Open Duck Mini v2 with long legs, a long neck, a wing on each side and a small bird's head.
What its parts share.

Its parts are the Duck's programs (robots/open_duck_mini_v2, beside this folder) and these:

  thigh_*_sheet, shin_*_sheet   the Duck's leg sheets, run with the Flamingo's THIGH and SHIN
  left_cache, right_cache       the Duck's leg covers, over the longer thigh's knee
  neck_*_sheet                  the Duck's neck sheets, run with its NECK
  wing_mount, wing              each wing: an STS3215 (the Duck's servo) lying out from the body's side, its
                                axis along x, so the wing flaps up and down about it (the same programs both sides)
  body_middle_top               the Duck's own shell with the wing mounts' screws, their cables, and the Pi
  roll_bracket, skull, nape, eye   the bird head (below)

Every other part is the Duck's own, unchanged.

The wings: wing_mount is the servo's cradle, a plate on each of its case's faces, screwed to the case as the
Duck's sheets are, and a base across its far end, screwed through the body's side wall (nuts inside); wing is
a yoke on the servo's horn and idler (as the Duck's head-pitch yoke) carrying the blade.

Frames: wing_mount and wing are drawn in the servo's own frame (ServoFaces): origin on the output axis at
the horn face, x = back (along the case to its far end), y = across, z = into the servo. The body's frame
is the Duck's shells' (body_middle_top's): x forward, y left, z up. PLACE puts the servo frame in it.
"""

import os
import runpy

HERE = os.path.dirname(os.path.realpath(__file__))
DUCK = os.path.join(os.path.dirname(HERE), "open_duck_mini_v2")     # the Duck's folder, beside this one
D = runpy.run_path(os.path.join(DUCK, "shared.py"))         # the Duck's shared values


def duck(part: str) -> str:
    """The Duck's program for a part."""
    for path in (os.path.join(DUCK, "parts", part + ".py"), os.path.join(DUCK, part, "written.py")):
        if os.path.exists(path):
            return path
    raise FileNotFoundError("the Duck has no part %s" % part)


# -- design: the Flamingo's -- free ----------------------------------------------------------------
# a flamingo's long bone is its lower leg; the Duck's thigh, shin and neck are 78.65, 78.65 and 66.0
THIGH = 150.0                              # the hip pitch's axis to the knee's
SHIN = 220.0                               # the knee's axis to the ankle's
NECK = 130.0                               # the neck pitch's axis to the head pitch's

# -- interfaces -- fixed ----------------------------------------------------------------------------
SERVO = D["SERVO"]                         # the Duck's STS3215
F = SERVO.faces
CLEARANCE = D["CLEARANCE"]                 # a screw's hole and head in a printed part, by thread
HORN = F.horn.rotated(-F.horn.first_deg)   # the horn's holes on the frame's axes, as the Duck's parts take them
IDLER = F.idler.rotated(-F.idler.first_deg)
M3_NUT = 6.4                               # across corners, for the nuts inside the shell
# the body's side wall: flat at y = WALL_Y from the shell's split line up to where the section turns in
WALL_Y = max(y for y, z in D["BODY_SECTION"])
WALL_T = 3.0                               # body_middle_top's WALL
FLAT_Z = (D["BODY_SPLIT_Z"], max(z for y, z in D["BODY_SECTION"] if y == WALL_Y))

# -- the cradle's fit to the case -----------------------------------------------------------------
CASE_FIT = 0.3                             # between the case's far end and the base
PLATE_T = 4.0                              # each face's plate (the idler face's raised middle takes 2.1 of it)
BASE_T = 7.0                               # the base: the screws' heads sink in it, flush under the case
FAR = F.case_back + CASE_FIT               # the base's inner face, back from the axis

# -- design: where the wing is ------------------------------------------------------------------------
# along x, the horn face: the base's screws' nuts land inside the shell between the shell's front inner frame
# and the trunk's hip tab (the clear band, x -20 .. +22 in the Duck's world, is 42 mm)
WING_X = 31.0
WING_Z = sum(FLAT_Z) / 2                   # centred on the flat of the wall
AXIS_Y = WALL_Y + BASE_T + FAR             # the axis this far out from the middle
BASE_SCREWS = [(7.0, 9.0), (31.0, -9.0)]   # the base's two M3s, (into, across): either side of the cable's window
CABLE_WINDOW = (11.0, 27.0, 7.0)           # through the base and the wall: into from-to, half across

# each side's servo frame in the body's: origin (the horn face on the axis), back, into; across = into x back
PLACE = {
    "left": dict(origin=(WING_X, AXIS_Y, WING_Z), back=(0, -1, 0), into=(-1, 0, 0)),
    "right": dict(origin=(WING_X, -AXIS_Y, WING_Z), back=(0, 1, 0), into=(-1, 0, 0)),
}


def to_body(side, p):
    """A point (back, across, into) of a side's servo frame, in the body's frame."""
    o, b, z = PLACE[side]["origin"], PLACE[side]["back"], PLACE[side]["into"]
    a = (z[1] * b[2] - z[2] * b[1], z[2] * b[0] - z[0] * b[2], z[0] * b[1] - z[1] * b[0])
    return tuple(o[i] + p[0] * b[i] + p[1] * a[i] + p[2] * z[i] for i in range(3))


# == the bird head ==================================================================================
# The Duck's head (200 x 200 x 60 mm round its yaw servo, the roll servo, the boards and the antennas'
# servos) is replaced by a small skull in front of the yaw servo. Four parts of ours, all in the Duck's
# vendor frame (x forward, z up, the head's middle at y = 0), as the Duck's head parts are:
#
#   roll_bracket   the Duck's yaw-to-roll U-bracket alone (no ring, no back journal), screwed to the yaw
#                  servo's far tabs as the Duck's is; its wall takes the roll servo's shaft
#   skull          a shell round the roll servo, a beak, and an eye socket each side; open at the back
#   nape           the plate closing the skull's back, round the bracket's shaft boss
#   eye            a domed eye pressed into each socket (one program, both sides)
#
# The roll servo is an SG90, the antennas' servo in the Duck: the head roll holds 0.027 N m at a full
# 90 deg tilt with the Duck's 361 g head (its centre 7.6 mm off the axis), against the SG90's 0.18.
# The Raspberry Pi and its board move to the trunk (body_middle_top); the antennas are dropped.

# -- interfaces -- fixed: the SG90 -----------------------------------------------------------------
# TowerPro SG90 as the Duck's model draws it (Open Duck Mini v2's Onshape assembly, Apache-2.0: sg90.stl,
# measured). Its own frame: z up the output shaft from the case's bottom, x along the case's length.
SG90_LENGTH = 23.0                         # the case: along x,
SG90_WIDTH = 13.0                          # across (y),
SG90_HEIGHT = 23.42                        # its bottom to its top (z)
SG90_SHAFT_X = 5.67                        # the shaft's axis, along x from the case's middle
SG90_TABS_Z = (16.7, 19.2)                 # the mounting tabs: bottom and top faces
SG90_TAB_HOLES_X = 13.75                   # their holes, each side of the case's middle,
SG90_TAB_HOLE_D = 2.0
SG90_TOWER_X = (-2.8, 11.5)                # the gear tower on the case's top: x from-to,
SG90_TOWER_WIDTH = 11.64
SG90_TOWER_TOP = 27.9
SG90_SHAFT_TOP = 30.97                     # the shaft's end
SG90_MASS_G = 9.0                          # TowerPro's data sheet
# the shaft's fit, as the Duck's antenna holder takes it: a bore over the spline, its screw through the end
SHAFT_BORE_D = 5.05
SHAFT_SCREW_D = 2.7
SHAFT_BOSS_D = 9.05                        # the bracket's boss round the bore (the antenna holder's tube); the nape clears it

# -- interfaces -- fixed: the Duck's head yaw and roll ----------------------------------------------
ROLL_Y, ROLL_Z = 0.0, 129.06               # the head roll axis, along x (the Duck's)
SHAFT_TIP_X = 60.95                        # the roll shaft's end on the bracket's wall (the Duck's horn seat)

# -- design: the skull -- free -------------------------------------------------------------------------
SKULL_X = 76.0                             # a spheroid about the roll axis: its middle along x,
SKULL_HALF_LONG = 40.0                     # half its length,
SKULL_R = 27.0                             # its radius
NAPE_X = 62.0                              # its back cut flat here (the bracket's wall is behind), the nape flush in it
NAPE_T = 2.0                               # the nape, from its back face to its seat on the skull's bosses
SKULL_WALL = 2.0
NAPE_SCREWS_Y = 17.0                       # the nape's two M2 screws, each side of the axis at its height
EYE_X = 88.0                               # each eye: along x,
EYE_UP = 7.0                               # above the roll axis,
EYE_PEG_D = 6.0                            # its peg's socket in the skull


def sg90_to_head(p):
    """A point (x, y, z) of the SG90's own frame in the head's: its shaft on the roll axis pointing back
    (-x) to the bracket's wall, its case's length hanging down (-z)."""
    x, y, z = p
    return (SHAFT_TIP_X + SG90_SHAFT_TOP - z, y, ROLL_Z + (x - SG90_SHAFT_X))


def skull_r(x, shrink=0.0):
    """The skull's radius about the roll axis at x (its outside; less `shrink` all round for its inside)."""
    a, b = SKULL_HALF_LONG - shrink, SKULL_R - shrink
    t = (x - SKULL_X) / a
    return b * (1 - t * t) ** 0.5 if abs(t) < 1 else 0.0


def eye_seat(side):
    """Where an eye's peg enters the skull (x, y, z): on its outside, EYE_UP above the roll axis; it points out along y."""
    s = 1 if side == "left" else -1
    return (EYE_X, ROLL_Y + s * (skull_r(EYE_X) ** 2 - EYE_UP ** 2) ** 0.5, ROLL_Z + EYE_UP)


# == the head's electronics, moved to the trunk ======================================================
# The Pi hangs from the top shell's ceiling (body_middle_top.py) on four standoffs, components down, turned
# across the body behind the shell's top window; the head's board -- the same board as the Duck's main
# board on the trunk top's deck, with the same holes -- stacks on that board on four bought M2 hex spacers.
# Both where the assembled trunk is clear, 2.5 mm from every part.
# Frame: the shells' (body_middle_top's): x forward, y left, z up.

# -- interfaces -- fixed ----------------------------------------------------------------------------
from yotown.gym.vendors.raspberrypi import PI_ZERO_2_W   # noqa: E402  (58 x 23 holes; the Duck's model: 58.06 x 23.04)
CEILING_Z = max(z for y, z in D["BODY_SECTION"]) - WALL_T  # the shell's inside, over the middle (its window is |y| < 25)
PI_HOLE_D = 2.2                            # M2.5 self-tapping, into each standoff

# -- design: where they go -- free ----------------------------------------------------------------------
PI_X = -65.0                               # the Pi's middle (its length across the body, along y)
PI_STANDOFF = 5.0                          # its board this far under the ceiling
STANDOFF_D = 6.0
BOARD_SPACER = 10.0                        # the head's board over the main board's top (bought M2 F-F spacers)


def pi_holes():
    """The Pi's four holes (x, y) in the shells' frame: its length along y."""
    hx, hy = PI_ZERO_2_W.holes.pitch
    return [(PI_X + sx * hy / 2, sy * hx / 2) for sx in (1, -1) for sy in (1, -1)]
