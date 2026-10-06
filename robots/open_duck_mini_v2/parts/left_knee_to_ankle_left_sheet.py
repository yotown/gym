"""Open Duck Mini v2 servo sheet -- the knee-to-ankle sheet (the outer one) -- written from its STEP:
interfaces exact, the body simple.

One design joins a servo's horn to the next servo's case; the duck uses it four times (the two
knee-to-ankle sheets of each leg, the two neck sheets). This program is the outer knee-to-ankle sheet;
the others run it with their differences (SHEET) and their place (PLACE).

LINK is the design's length: the horn's axis to the next servo's (the leg's thigh and shin, 78.65; the
neck's link, 66). Everything at the foot end -- the next servo's seat, its screws, the foot -- is placed
back from that axis, so a longer link moves the seat and keeps the servo's fit.

A plate: round about the horn's axis at one end, a rectangle at the other (the foot), its sides leaning
in between; its outer face's edges chamfered. On its inner face the horn sits, held by four screws
counterbored from the outer face; a slot runs from the horn's bore to the round end. Behind the foot a
block reaches in to the next servo: a pocket for its case, a narrower step in its floor, two screws,
a cable slot. Rods may pass through the plate between (the leg spacer's).

Frame: the sheet's own, (u, v, w) in mm: the origin on the horn's axis in the face the horn sits on,
v from the horn towards the foot, w out through the plate (the plate is w in [0, THICK]). Every
interface is a level in w from that seat -- the next servo's seat, each screw head's -- so the plate's
thickness, the block and the rims are free. PLACE puts it in the vendor's frame: the horn's seat on its
axis, v's direction and w's.
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the Duck's shared values (../shared.py)
SERVO, HORN, HORN_SCREW = S.SERVO, S.HORN, S.HORN_SCREW

H = globals().get("SHEET", {})             # the other sheets' differences
PLACE = globals().get("PLACE", dict(origin=(-16.06, 109.15, -143.65), v=(0, 0, -1), w=(0, 1, 0)))   # the outer knee-to-ankle sheet

# -- interfaces -- fixed ----------------------------------------------------------------------------
LINK = H.get("link", 78.65)                # the horn's axis to the next servo's horn axis (along v)
# the horn, on the seat (w = 0)
HORN_THROUGH_D = 7.0                       # through, on its axis
HORN_SCREW_HEAD_SEAT = H.get("horn_head_w", 2.9)   # its seat (w)
RODS = H.get("rods", True)                 # the leg spacer's rods through, or none:
ROD_V = 20.325
ROD_D = 3.2
ROD_HEAD_D = 6.5
ROD_HEAD_SEAT = H.get("rod_head_w", 1.9)   # (w)
# the next servo, its case on the pocket's floor; each from that far back from its axis (v = LINK - back)
SERVO_SEAT_W = H.get("servo_seat_w", -3.15)   # the case's face on the pocket's floor
POCKET_W = H.get("pocket_w", 24.7)         # the case's pocket: wide,
POCKET_BACK = H.get("pocket_back", 35.11)  # back
STEP = H.get("step", True)                 # a narrower, deeper step in its floor, or none:
STEP_W = H.get("step_w", 14.0)
STEP_DEEP = H.get("step_deep", 1.1)        # below the seat
SERVO_SCREW_BACK = H.get("servo_back", 29.0)
SERVO_SCREW_HEAD_D = 5.0
SERVO_SCREW_HEAD_SEAT = H.get("servo_head_w", -1.1)   # (w)

# -- body: free -------------------------------------------------------------------------------------
STEP_BACK = H.get("step_back", 35.11)      # the step, from this far back
THICK = H.get("thick", 3.9)
FOOT_BACK = H.get("foot_back", 19.0)       # the plate's foot: back from the next servo's axis,
FOOT_W = H.get("foot_w", 30.7)             # this wide
LEAN_FROM_V = H.get("lean_from_v", 33.54)  # nearer the horn than this the sides lean in,  # measured
LEAN_DEG = H.get("lean_deg", 7.24)         # measured
ROUND_R = 11.0                             # the round end, about the horn's axis
CHAMFER = 1.0                              # the outer face's edges
BLOCK_BACK = H.get("block_back", 38.11)    # the block behind the foot, from this far back (within the plate's outline)
RIM = H.get("rim", 1.4)                    # the pocket's rim stands this far past the seat
CABLE = "cable_w" in H                     # a slot for the cable up the block, or none:
CABLE_W = H.get("cable_w")
CABLE_BACK = H.get("cable_back")
CABLE_TOP_W = H.get("cable_top_w")         # up to w,
CABLE_END_R = H.get("cable_end_r")         # its end round about w = CABLE_END_W
CABLE_END_W = H.get("cable_end_w")
RELIEF_W = 7.6                             # clears the horn: from its bore to the round end, in the seat,
RELIEF_DEEP = H.get("inner_bore_deep", 1.4)
RELIEF_R = 1.0                             # its corners
HUB_D = 7.6                                # and the horn's hub, into the seat as deep
FOOT_V = LINK - FOOT_BACK
BLOCK_FROM = LINK - BLOCK_BACK


def at_w(w):
    """The plane w = const, (u, v) its coordinates; extrude(d) goes d towards +w."""
    return cq.Workplane(cq.Plane(origin=(0, 0, w), xDir=(1, 0, 0), normal=(0, 0, 1)))


def towards_foot(v_from, wide):
    """A rectangle from v_from to past the foot, centred on u = 0."""
    return lambda wp: wp.center(0, (v_from + FOOT_V + 1) / 2).rect(wide, FOOT_V + 1 - v_from)


half = FOOT_W / 2
lean = half - math.tan(math.radians(LEAN_DEG)) * LEAN_FROM_V   # half the width at the horn's axis
outline = [(-half, FOOT_V), (half, FOOT_V), (half, LEAN_FROM_V), (lean, 0), (-lean, 0), (-half, LEAN_FROM_V)]
plate = at_w(0).polyline(outline).close().extrude(THICK)
plate = plate.union(at_w(0).circle(ROUND_R).extrude(THICK)).faces(">Z").edges().chamfer(CHAMFER)

# the block behind the foot, from the pocket's rim to the seat; the case's pocket in it, a step in its floor
rim = SERVO_SEAT_W - RIM                   # the block's face
sheet = plate.union(towards_foot(BLOCK_FROM, FOOT_W)(at_w(rim)).extrude(-rim).intersect(at_w(rim).polyline(outline).close().extrude(-rim)))
sheet = sheet.cut(towards_foot(LINK - POCKET_BACK, POCKET_W)(at_w(rim - 1)).extrude(SERVO_SEAT_W - rim + 1))
if STEP:
    sheet = sheet.cut(towards_foot(LINK - STEP_BACK, STEP_W)(at_w(SERVO_SEAT_W)).extrude(STEP_DEEP))
if CABLE:
    sheet = sheet.cut(towards_foot(LINK - CABLE_BACK, CABLE_W)(at_w(rim - 1)).extrude(CABLE_TOP_W - rim + 1))
    sheet = sheet.cut(cq.Workplane("YZ", origin=(-CABLE_W / 2, 0, 0)).center(LINK - CABLE_BACK, CABLE_END_W).circle(CABLE_END_R).extrude(CABLE_W))

sheet = sheet.cut(at_w(0).center(0, -ROUND_R).rect(RELIEF_W, 2 * ROUND_R).extrude(RELIEF_DEEP).edges("|Z").fillet(RELIEF_R))

# -- interfaces, cut last -------------------------------------------------------------------------
low = min(rim, 0) - 1                      # through: from below the lowest face ...
span = THICK - low + 1                     # ... to past the outer one
through = at_w(low)
sheet = sheet.cut(at_w(0).circle(HUB_D / 2).extrude(RELIEF_DEEP)).cut(through.circle(HORN_THROUGH_D / 2).extrude(span))


def screws(pts, d, head_d, head_w):
    """Holes through, each with its head's seat at head_w and room for the head out past the outer face."""
    global sheet
    sheet = sheet.cut(through.pushPoints(pts).circle(d / 2).extrude(span))
    sheet = sheet.cut(at_w(head_w).pushPoints(pts).circle(head_d / 2).extrude(THICK - head_w + 1))


screws(HORN.points(), HORN_SCREW.hole_d, HORN_SCREW.head_d, HORN_SCREW_HEAD_SEAT)
if RODS:
    screws([(-S.LEG_ROD_PITCH / 2, ROD_V), (S.LEG_ROD_PITCH / 2, ROD_V)], ROD_D, ROD_HEAD_D, ROD_HEAD_SEAT)
v = LINK - SERVO_SCREW_BACK
screws([(-SERVO.tab_half_pitch, v), (SERVO.tab_half_pitch, v)], S.SERVO_SCREW_D, SERVO_SCREW_HEAD_D, SERVO_SCREW_HEAD_SEAT)

# into the vendor's frame: u = v x w
v, w = cq.Vector(*PLACE["v"]), cq.Vector(*PLACE["w"])
frame = cq.Plane(origin=PLACE["origin"], xDir=v.cross(w), normal=w)
result = cq.Workplane(obj=sheet.val().transformShape(frame.rG))
