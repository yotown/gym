"""LeRobot humanoid upper torso, written from its STEP: a 45 mm slab whose outline is a column with
shoulders and a V top, and at each shoulder a tilted ring that seats the shoulder's bearing.

Frame: the STEP's (mm). The slab spans x -22.5 .. 22.5, the column stands on z = 0, the part is
symmetric about y = 0: the +y shoulder is modelled and each of its tools mirrored. A shoulder's ring
has its own frame: its axis (measured), x the -x direction projected onto the ring's plane.
Approximated: the shoulder ends are free-form in the STEP; here one straight edge (SHOULDER_END)
that lies mostly inside the ring's pocket."""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)
M3 = S.M3

# -- interfaces -- fixed: the shoulder's bearing ring (one side; the other is its mirror) ----------
RING_AXIS = (-0.6782, 0.5279, 0.5113)       # measured
RING_ORIGIN = (5.881, 95.914, 223.306)      # on the axis: the ring's bottom face  # measured
RING_D = 65.0
SEAT_D, SEAT_FROM = 57.0, 15.0              # the bearing's seat: its floor above the ring's bottom; not in the model: the bearing
M3_CBORE_TO = 10.0                          # the counterbore, to 10 up the axis; not in the model: the M3 screws
M3_CIRCLE_D = 50.0
PIN_D, PIN_CIRCLE_D = 3.0, 60.0             # six, blind, between the screws (30 deg)
PIN_TO = 10.0                               # not in the model: the pins

# -- body: free -------------------------------------------------------------------------------------
RING_H = 30.0                               # the ring's top, above the bearing's seat
SPIGOT_D, SPIGOT_H = 44.6, 2.0              # a lip, centred on the ring's bottom face
BORE_D = 43.0                               # through, under the bearing
THICKNESS = 45.0
COLUMN_W = 85.878
SHOULDER_Z = 205.0
NECK_Z = 230.0                             # the V top: apex at y 0, rising this much per mm of |y|
V_SLOPE = 17.5 / 55.0
SHOULDER_END = (95.0, 83.0)                 # |y| at the ledge, |y| at the top  # measured
POCKET_DEPTH = 48.594                       # the ring's clearance pocket, below it  # measured
RELIEF_D = 10.0                            # measured
RELIEF_FROM = (6.782, 21.331)
RELIEF_AT = (30.364, 100.160, 251.392)
TOP_ROUND_R = 5.0                           # along the +x edges of the V top

# the slab: the half outline, mirrored about y = 0
w, (y_ledge, y_top) = COLUMN_W / 2, SHOULDER_END
half = [(0, 0), (w, 0), (w, SHOULDER_Z), (y_ledge, SHOULDER_Z), (y_top, NECK_Z + y_top * V_SLOPE), (0, NECK_Z)]
torso = cq.Workplane("YZ", origin=(-THICKNESS / 2, 0, 0)).polyline(half).mirrorY().extrude(THICKNESS)
torso = torso.faces(">X").edges(cq.selectors.BoxSelector((0, -y_top, NECK_Z + 5), (THICKNESS, y_top, 300))).fillet(TOP_ROUND_R)

# the +y shoulder ring's frame
axis = cq.Vector(RING_AXIS).normalized()
across = cq.Vector(-1, 0, 0)
ring = cq.Plane(origin=RING_ORIGIN, xDir=(across - axis * across.dot(axis)).normalized(), normal=axis)


def both(tool):
    """A +y shoulder tool and its mirror at the -y shoulder."""
    return tool.union(tool.mirror("XZ"))


def on_ring(t):
    return cq.Workplane(ring).workplane(offset=t)


torso = torso.cut(both(on_ring(-POCKET_DEPTH).circle(RING_D / 2).extrude(POCKET_DEPTH)))
torso = torso.union(both(on_ring(0).circle(RING_D / 2).extrude(RING_H)))
torso = torso.union(both(on_ring(-SPIGOT_H / 2).circle(SPIGOT_D / 2).extrude(SPIGOT_H)))
torso = torso.cut(both(on_ring(-SPIGOT_H).circle(BORE_D / 2).extrude(SEAT_FROM + SPIGOT_H)))
torso = torso.cut(both(on_ring(SEAT_FROM).circle(SEAT_D / 2).extrude(RING_H - SEAT_FROM + 1)))
screws = on_ring(-SPIGOT_H).polarArray(M3_CIRCLE_D / 2, 0, 360, 6)
torso = torso.cut(both(screws.circle(M3.head_d / 2).extrude(M3_CBORE_TO + SPIGOT_H)))
torso = torso.cut(both(on_ring(0).polarArray(M3_CIRCLE_D / 2, 0, 360, 6).circle(M3.hole_d / 2).extrude(SEAT_FROM)))
torso = torso.cut(both(on_ring(-SPIGOT_H / 2).polarArray(PIN_CIRCLE_D / 2, 30, 360, 6).circle(PIN_D / 2)
                       .extrude(PIN_TO + SPIGOT_H / 2)))
relief = cq.Workplane(cq.Plane(origin=RELIEF_AT, xDir=ring.xDir, normal=axis)).workplane(offset=RELIEF_FROM[0])
result = torso.cut(both(relief.circle(RELIEF_D / 2).extrude(RELIEF_FROM[1])))
