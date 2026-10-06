"""LeRobot humanoid hip yaw link (hip_z 12), written from its STEP: interfaces exact, the body simple.

A ring on a column. The column stands on the hip-yaw axis (z, at x = y = 0): six screws down through
its floor, three pins under it. The ring, tilted, takes hip_z 22's plate: its bolt circles are that
plate's, in that plate's frame (ORIGIN, S.HIPZ_X_DIR, S.HIPZ_NORMAL, as hip_z22's program measures them). A thin
fin leaves the column for a cable.

Frame: the vendor's (mm); the ring's offsets are along S.HIPZ_NORMAL from RING_AT, a point on its axis.
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)
M3 = S.M3

# -- interfaces -- fixed ----------------------------------------------------------------------------
RING_AT = (-23.75, 36.18, -29.41)          # a point on the ring's axis  # measured
M4S = (90.0, 22.9, 45.0, (-1, 0, 1, 2), 4.3, (0.71, 30.71))    # through the wall: circle, first deg, pitch, which, d, along the axis from-to
M3S = (73.0, 2.8, 40.0, (-1, 0, 1, 2, 3, 4), 3.3, 6.5, (23.71, 26.71, 35.71))   # counterbored from the top: circle, first, pitch, which, d, head d, floor-seat-top
M35S = (90.0, (142.3, 157.1), 3.9, (-12.0, 30.71))  # M3.5, from below: circle, angles, d, from-to  # measured
TAP = (86.0, -10.0, 3.1, (13.2, 30.71))    # an M3 tapping hole: circle, angle, d, from-to
COLUMN = (35.0, -100.0)                    # the hip-yaw column: diameter, its foot
COLUMN_SCREWS = (27.0, 17.0, 6, 3.3, 6.5, 3.0)   # down through its floor: circle, first deg, count, d, head d, floor
COLUMN_PINS = (24.4, 47.0, 3, 3.0, 10.0)   # under it: circle, first deg, count, d, depth  # measured
RING = (100.0, 78.5, (1.0, 30.71))         # outside, bore, along the axis from-to  # measured
FLANGE = (60.0, 23.71)                     # an inward flange at its top: bore, from (along the axis)  # measured
LIP = (70.0, 66.0, 5.0)                    # a lip on top: outside, inside, tall  # measured
COLUMN_TOP = -15.8                         # measured
FIN = ((25.44, -38.76), 5.0, (-60.9, -55.9))   # a fin from the column: its round end, width, z from-to  # measured

# -- body: free -------------------------------------------------------------------------------------
NECK = (-9.0, 135.0, 225.0)                # towards the column the wall reaches further down: to, between angles (deg)  # measured

n = cq.Vector(*S.HIPZ_NORMAL)
ring_plane = lambda along: cq.Plane(origin=cq.Vector(*RING_AT) + n * along, xDir=S.HIPZ_X_DIR, normal=S.HIPZ_NORMAL)
od, bore, (r0, r1) = RING
hip = cq.Workplane(ring_plane(r0)).circle(od / 2).circle(bore / 2).extrude(r1 - r0)
to, a0, a1 = NECK
sector = (cq.Workplane(ring_plane(to)).moveTo(0, 0).lineTo(od * math.cos(math.radians(a0)), od * math.sin(math.radians(a0)))
          .threePointArc((od * math.cos(math.radians((a0 + a1) / 2)), od * math.sin(math.radians((a0 + a1) / 2))),
                         (od * math.cos(math.radians(a1)), od * math.sin(math.radians(a1)))).close().extrude(r0 - to))
hip = hip.union(cq.Workplane(ring_plane(to)).circle(od / 2).circle(bore / 2).extrude(r0 - to).intersect(sector))
hip = hip.union(cq.Workplane(ring_plane(FLANGE[1])).circle(od / 2).circle(FLANGE[0] / 2).extrude(r1 - FLANGE[1]))
hip = hip.union(cq.Workplane(ring_plane(r1)).circle(LIP[0] / 2).circle(LIP[1] / 2).extrude(LIP[2]))

# the column, its top trimmed where it meets the ring's bore
d, foot = COLUMN
column = cq.Workplane("XY", origin=(0, 0, foot)).circle(d / 2).extrude(COLUMN_TOP - foot)
column = column.cut(cq.Workplane(ring_plane(r0 - 40)).circle(bore / 2).extrude(FLANGE[1] - r0 + 40))
hip = hip.union(column)
(fx, fy), w, (z0, z1) = FIN
hip = hip.union(cq.Workplane("XY", origin=(0, 0, z0)).center(fx / 2, fy / 2)
                .slot2D(math.hypot(fx, fy) + w, w, math.degrees(math.atan2(fy, fx))).extrude(z1 - z0))

# -- interfaces, cut last -------------------------------------------------------------------------
def on_circle(c, angles):
    return [(c / 2 * math.cos(math.radians(a)), c / 2 * math.sin(math.radians(a))) for a in angles]


c, first, pitch, which, d, (a0, a1) = M4S
hip = hip.cut(cq.Workplane(ring_plane(a0)).pushPoints(on_circle(c, [first + k * pitch for k in which])).circle(d / 2).extrude(a1 - a0))
c, first, pitch, which, d, head, (f, s, t) = M3S
pts = on_circle(c, [first + k * pitch for k in which])
hip = hip.cut(cq.Workplane(ring_plane(f)).pushPoints(pts).circle(d / 2).extrude(t - f))
hip = hip.cut(cq.Workplane(ring_plane(s)).pushPoints(pts).circle(head / 2).extrude(t - s + 1))
c, angles, d, (a0, a1) = M35S
hip = hip.cut(cq.Workplane(ring_plane(a0)).pushPoints(on_circle(c, angles)).circle(d / 2).extrude(a1 - a0))
c, a, d, (a0, a1) = TAP
hip = hip.cut(cq.Workplane(ring_plane(a0)).pushPoints(on_circle(c, [a])).circle(d / 2).extrude(a1 - a0))
c, first, count, d, head, floor = COLUMN_SCREWS
pts = on_circle(c, [first + k * 360 / count for k in range(count)])
hip = hip.cut(cq.Workplane("XY", origin=(0, 0, foot)).pushPoints(pts).circle(d / 2).extrude(floor))
hip = hip.cut(cq.Workplane("XY", origin=(0, 0, foot + floor)).pushPoints(pts).circle(head / 2).extrude(120))
c, first, count, d, depth = COLUMN_PINS
hip = hip.cut(cq.Workplane("XY", origin=(0, 0, foot)).pushPoints(on_circle(c, [first + k * 360 / count for k in range(count)]))
              .circle(d / 2).extrude(depth))

result = hip
