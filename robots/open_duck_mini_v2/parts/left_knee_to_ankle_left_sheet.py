"""Open Duck Mini v2 servo sheet -- the knee-to-ankle sheet (the outer one) -- written from its STEP:
interfaces exact, the body simple.

One design joins a servo's horn to the next servo's case; the duck uses it four times (the two
knee-to-ankle sheets of each leg, the two neck sheets). This program is the outer knee-to-ankle sheet;
the others run it with their differences (SHEET) and their place (PLACE).

LINK is the design's length: the horn's axis to the next servo's (the leg's thigh and shin, 78.65; the
neck's link, 66). Everything at the foot end -- the next servo's seat, its screws, the foot -- is placed
back from that axis, so a longer link moves the seat and keeps the servo's fit.

The servos are choices (HORN_SERVO at the round end, CASE_SERVO at the foot end, from the Duck's SERVOS):
every fit to them -- the horn's holes and hub, the case's pocket, the step for its face's raised middle,
its screws, the seat's depth, the idler side's place -- is read from the servo's faces (ServoFaces).

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

H = globals().get("SHEET", {})             # the other sheets' differences
SIDE = H.get("side", "horn")               # the servos' side it is on: "horn" (this, the outer sheet) or "idler"

# -- interfaces -- fixed ----------------------------------------------------------------------------
HORN_SERVO = S.SERVOS["sts3215"]           # the servo whose horn (or idler) it takes, at its round end
CASE_SERVO = S.SERVOS["sts3215"]           # the next servo, whose case it holds, at its foot end
LINK = H.get("link", 78.65)                # the horn's axis to the next servo's horn axis (along v)
# where it sits: the horn servo's horn face on its axis (the leg's outer plane), and the way into the
# servos from it, in the vendor's frame; the next servo's horn face is in the same plane
HORN_FACE = (-16.06, 109.15, -143.65)
INTO = (0, -1, 0)
V = (0, 0, -1)                             # along the link, towards the next servo
# the horn (or the idler), on the seat (w = 0)
hf, cf = HORN_SERVO.faces, CASE_SERVO.faces
horn = hf.horn if SIDE == "horn" else hf.idler
HORN_HOLES = horn.rotated(-horn.first_deg)   # the horn clocked so its holes lie on the frame's axes
HORN_SCREW = S.CLEARANCE[hf.horn_thread]
HUB_D, HUB_PROUD = (hf.hub_d, hf.hub_proud) if SIDE == "horn" else (hf.idler_hub_d, hf.idler_hub_proud)
HORN_THROUGH_D = HUB_D + 1.0               # through, on its axis
HORN_HEAD_OVER_RELIEF = 1.5                # its seat (w): 2.9, or this far over the hub's relief if a taller hub needs it
RODS = H.get("rods", True)                 # the leg spacer's rods through, or none:
ROD_V = 20.325
ROD_D = 3.2
ROD_HEAD_D = 6.5
ROD_HEAD_SEAT = H.get("rod_head_w", 1.9)   # (w)
# the next servo, its case's face (on this side) on the pocket's floor; each from that far back from its axis (v = LINK - back)
face = cf.side(SIDE)
seat_depth = 0.0 if SIDE == "horn" else hf.idler_face   # this sheet's seat, from the outer plane into the servos
SERVO_SEAT_W = H.get("servo_seat_w", (seat_depth - face.level) if SIDE == "horn" else (face.level - seat_depth))
POCKET_FIT = -0.02                         # the case's pocket: as wide as the case, less this (a press fit),
POCKET_W = H.get("pocket_w", cf.case_width + POCKET_FIT)
POCKET_BACK = H.get("pocket_back", cf.case_back)   # back to its far end
STEP = H.get("step", True) and face.boss is not None   # a narrower, deeper step in its floor, for the face's raised middle, or none:
STEP_W, STEP_BACK, STEP_DEEP = face.boss if STEP else (None, None, None)
SERVO_SCREW = S.CLEARANCE[face.thread]
FOOT_BACK = H.get("foot_back", 19.0)       # the plate's foot: back from the next servo's axis (the screws it reaches are further back)
SERVO_SCREWS = [(across, back) for back, across in face.screws if back > FOOT_BACK]
if "servo_back" in H:                      # a sheet that takes the screws elsewhere
    SERVO_SCREWS = [(s * S.SERVO.tab_half_pitch, H["servo_back"]) for s in (-1, 1)]
SERVO_SCREW_GRIP = H.get("servo_grip", 2.05)   # under each screw's head, to the case's face
SERVO_SCREW_HEAD_SEAT = H.get("servo_head_w", SERVO_SEAT_W + SERVO_SCREW_GRIP)   # (w)

# -- body: free -------------------------------------------------------------------------------------
THICK = H.get("thick", 3.9)
SIDE_WALL = 3.0                            # this wide: the case's pocket with a wall each side
FOOT_W = H.get("foot_w", POCKET_W + 2 * SIDE_WALL)
LEAN_FROM_V = H.get("lean_from_v", 33.54)  # nearer the horn than this the sides lean in,  # measured
LEAN_DEG = H.get("lean_deg", 7.24)         # measured
ROUND_R = 11.0                             # the round end, about the horn's axis
CHAMFER = 1.0                              # the outer face's edges
BACK_WALL = 3.0                            # the block behind the foot: the pocket's back wall,
BLOCK_BACK = H.get("block_back", POCKET_BACK + BACK_WALL)   # from this far back (within the plate's outline)
RIM = H.get("rim", 1.4)                    # the pocket's rim stands this far past the seat
CABLE = "cable_w" in H                     # a slot for the cable up the block, or none:
CABLE_W = H.get("cable_w")
CABLE_BACK = H.get("cable_back", BLOCK_BACK)   # through the back wall
CABLE_TOP_W = H.get("cable_top_w")         # up to w,
CABLE_END_R = H.get("cable_end_r")         # its end round about w = CABLE_END_W, meeting its top
CABLE_END_W = H.get("cable_end_w", CABLE_TOP_W - CABLE_END_R if CABLE else None)
RELIEF_W = HUB_D + 1.6                     # clears the horn: from its bore to the round end, in the seat,
RELIEF_DEEP = max(H.get("inner_bore_deep", 1.4), HUB_PROUD + 0.5)
RELIEF_R = 1.0                             # its corners
HUB_BORE_D = HUB_D + 1.6                   # and the horn's hub, into the seat as deep
HORN_SCREW_HEAD_SEAT = H.get("horn_head_w", max(2.9, RELIEF_DEEP + HORN_HEAD_OVER_RELIEF))
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
sheet = sheet.cut(at_w(0).circle(HUB_BORE_D / 2).extrude(RELIEF_DEEP)).cut(through.circle(HORN_THROUGH_D / 2).extrude(span))


def screws(pts, d, head_d, head_w):
    """Holes through, each with its head's seat at head_w and room for the head out past the outer face."""
    global sheet
    sheet = sheet.cut(through.pushPoints(pts).circle(d / 2).extrude(span))
    sheet = sheet.cut(at_w(head_w).pushPoints(pts).circle(head_d / 2).extrude(THICK - head_w + 1))


screws(HORN_HOLES.points(), HORN_SCREW.hole_d, HORN_SCREW.head_d, HORN_SCREW_HEAD_SEAT)
if RODS:
    screws([(-S.LEG_ROD_PITCH / 2, ROD_V), (S.LEG_ROD_PITCH / 2, ROD_V)], ROD_D, ROD_HEAD_D, ROD_HEAD_SEAT)
screws([(across, LINK - back) for across, back in SERVO_SCREWS], SERVO_SCREW.hole_d, SERVO_SCREW.head_d, SERVO_SCREW_HEAD_SEAT)

# into the vendor's frame: u = v x w; the idler side's seat is the horn servo's idler face, looking the other way
into = cq.Vector(*INTO)
PLACE = globals().get("PLACE") or dict(origin=(cq.Vector(*HORN_FACE) + into * seat_depth).toTuple(), v=V,
                                       w=(-into if SIDE == "horn" else into).toTuple())
v, w = cq.Vector(*PLACE["v"]), cq.Vector(*PLACE["w"])
frame = cq.Plane(origin=PLACE["origin"], xDir=v.cross(w), normal=w)
result = cq.Workplane(obj=sheet.val().transformShape(frame.rG))
