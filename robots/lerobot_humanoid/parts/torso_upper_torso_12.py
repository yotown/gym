"""LeRobot humanoid upper torso, the +x half of the shoulder bar, written from its STEP: interfaces exact,
the body simple. torso_uper_torso_22, the -x half, runs this program with its differences (HALF).

Frame: the vendor's (the torso's STEP frame, mm): the bar runs along y, symmetric about y = Y_MID; the
two halves meet on the plane x = SPLIT_X (this one is x > SPLIT_X; torso_uper_torso_22 is the other).
A U-section beam (a thick floor, a flange on the split face, a rail on the outside) between two half
rings, one round each shoulder actuator, tilted 8 deg; a tab at each end for the bolt that closes
the ring with the other half.
"""

import math

import cadquery as cq

# -- interfaces -- fixed ----------------------------------------------------------------------------
Y_MID = 3.49                               # the bar's middle: everything is mirrored about it
SPLIT_X = 0.46                             # the face the two halves meet on
BOLTS_ACROSS = (5.2, -109.04, 75.0)        # three bolts through the split flange to the other half: d, z, pitch along y
BORES = (10.0, -109.1, 75.0)               # three bores across the bar (along x), on the same stations: d, z, pitch
END_BOLT = (4.5, -107.79, 177.965)         # an M4 through each end tab: d, z, from the middle
TAB_HOLES = (2.4, 39.1, (-21.01, 27.99))   # two holes down through the middle tab: d, x, y
FLOOR = (-133.1, -113.84)                  # the beam's floor: bottom, top  # measured
RING_FROM_MID = 140.785                    # each shoulder ring's centre, from the middle (along y); not in the model: this part (the model has no upper torso)
RING_Z = -127.7                            # the ring's underside, at its centre; not in the model: this part (the model has no upper torso)
RING_TILT_DEG = 8.1                        # the ring's axis leans in, towards the bar's middle; not in the model: this part (the model has no upper torso)  # measured
SEAT = (41.1, 4.0)                         # the actuator's seat in the ring's foot: diameter, depth; not in the model: this part (the model has no upper torso)

# -- body: free -------------------------------------------------------------------------------------
OUTER_X = 35.2                             # measured
FLANGE = (4.54, -104.27)                   # the split face's flange: thick, up to z  # measured
RAIL = (24.6, -102.6)                      # the outer rail: from x, up to z  # measured
BEAM_Y = 86.645                            # the full-depth beam runs between y -BEAM_Y and +BEAM_Y (about y 0, not the middle)  # measured
NECK = (12.45, 106.5)                      # past the beam, the floor is full depth only from this x, to this far out  # measured
PLATE = (-128.82, 118.15)                  # and from the split face a plate: its top, how far out it runs  # measured
RING_R = (29.3, 35.0)                      # the ring: inside, outside  # measured
RING_HEIGHT = 29.0                         # along its axis  # measured
END_TAB = (5.0, (-122.4, -93.0), (166.5, 185.0))   # each end tab: thick, z from-to, from the middle from-to  # measured
MIDDLE_TAB = (42.73, (-28.0, 28.0))        # a tab on the outside under the middle: out to x, along y about the middle  # measured


H = globals().get("HALF", {})              # the other half's differences (torso_uper_torso_22 passes them)


def box(x, y, z):
    return (cq.Workplane("XY").box(x[1] - x[0], y[1] - y[0], z[1] - z[0])
            .translate(((x[0] + x[1]) / 2, (y[0] + y[1]) / 2, (z[0] + z[1]) / 2)))


def about_mid(a, b):
    """y from a to b measured from the middle, as a (low, high) pair."""
    return (Y_MID + a, Y_MID + b)


bottom, floor_top = FLOOR
# the beam: floor, flange, rail
bar = box((SPLIT_X, OUTER_X), (-BEAM_Y, BEAM_Y), FLOOR)
bar = bar.union(box((SPLIT_X, SPLIT_X + FLANGE[0]), (-BEAM_Y, BEAM_Y), (floor_top, FLANGE[1])))
bar = bar.union(box((RAIL[0], OUTER_X), about_mid(-RING_FROM_MID, RING_FROM_MID), (floor_top, RAIL[1])))
if H.get("middle_tab", True):
    bar = bar.union(box((OUTER_X, MIDDLE_TAB[0]), about_mid(*MIDDLE_TAB[1]), FLOOR))

# one end (the -y side), mirrored to the other: the neck, the plate, the ring, the end tab
inner = -75.0                             # the end pieces reach into the beam far enough to meet it on both sides once mirrored
end = box((NECK[0], OUTER_X), (Y_MID - NECK[1], inner), FLOOR)
end = end.union(box((SPLIT_X, OUTER_X), (Y_MID - PLATE[1], inner), (bottom, PLATE[0])))
tilt = math.radians(RING_TILT_DEG)
centre = (SPLIT_X, Y_MID - RING_FROM_MID, RING_Z)
plane = cq.Plane(origin=centre, xDir=(1, 0, 0), normal=(0, math.sin(tilt), math.cos(tilt)))
ring = cq.Workplane(plane).circle(RING_R[1]).extrude(RING_HEIGHT)
ring = ring.union(cq.Workplane(plane).center(OUTER_X / 2, RING_R[1] / 2).rect(OUTER_X, RING_R[1]).extrude(RING_HEIGHT))   # solid towards the middle
ring = ring.cut(cq.Workplane(plane).circle(RING_R[0]).extrude(RING_HEIGHT))
ring = ring.union(cq.Workplane(plane).circle(RING_R[1]).circle(SEAT[0] / 2).extrude(SEAT[1]))
ring = ring.intersect(box((SPLIT_X, OUTER_X + 1), (centre[1] - 50, centre[1] + 50), (bottom, -80)))   # the +x half, above the floor
ring = ring.cut(box((SPLIT_X - 1, NECK[0]), (centre[1], centre[1] + 50), (bottom - 1, -80)))   # on the middle side, only beyond the neck
end = end.union(ring)
t, (z0, z1), (a, b) = END_TAB
end = end.union(box((SPLIT_X, SPLIT_X + t), about_mid(-b, -a), (z0, z1)))
bar = bar.union(end).union(end.mirror("XZ", basePointVector=(0, Y_MID, 0)))
bore = cq.Workplane(plane).workplane(offset=SEAT[1]).circle(RING_R[0]).extrude(RING_HEIGHT)   # clear of the beam and rail, above the seat
bar = bar.cut(bore).cut(bore.mirror("XZ", basePointVector=(0, Y_MID, 0)))

# -- interfaces, cut last -------------------------------------------------------------------------
d, z, pitch = BOLTS_ACROSS
d = H.get("bolt_d", d)
stations = [Y_MID - pitch, Y_MID, Y_MID + pitch]
bar = bar.cut(cq.Workplane("YZ", origin=(SPLIT_X - 1, 0, 0)).pushPoints([(y, z) for y in stations]).circle(d / 2).extrude(FLANGE[0] + 2))
d, z, _ = BORES
if H.get("bores", True):
    bar = bar.cut(cq.Workplane("YZ", origin=(SPLIT_X + 10.2, 0, 0)).pushPoints([(y, z) for y in stations]).circle(d / 2).extrude(OUTER_X))
d, z, r = END_BOLT
bar = bar.cut(cq.Workplane("YZ", origin=(SPLIT_X - 1, 0, 0)).pushPoints([(Y_MID - r, z), (Y_MID + r, z)]).circle(d / 2).extrude(END_TAB[0] + 2))
d, x, ys = TAB_HOLES
x = H.get("tab_holes_x", x)
bar = bar.cut(cq.Workplane("XY", origin=(0, 0, bottom - 1)).pushPoints([(x, y) for y in ys]).circle(d / 2).extrude(floor_top - bottom + 2))

if H.get("mirror"):                       # the other half: the same bar, mirrored across the split face
    bar = bar.mirror("YZ", basePointVector=(SPLIT_X, 0, 0))
result = bar
