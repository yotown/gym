"""Open Duck Mini v2 leg cover (the left leg's "cache"), written from its STEP: interfaces exact, the body
simple. right_cache is this part mirrored across the robot's middle (y = 0).

A shell over the thigh, all of it set out from one polygon (CORNERS: its front face, each corner the
centre of an R10 round): the front plate is that polygon grown by R10, drafted in to the polygon itself
at the front; the wall behind it is the band between R10 and R10 less the wall's thickness, cut open
towards the back of the leg between two end caps. Two bosses behind the plate take the screws that hold
it to the leg, counterbored from the front.

Frame: the vendor's (mm). The cover's section is in (x, z); it runs along y from BACK to FRONT.
"""

import math

import cadquery as cq

# -- interfaces -- fixed ----------------------------------------------------------------------------
SCREW_X = [-24.06, -8.06]                  # into the leg sheet's outer face: x,
SCREW_Z = -85.325
SCREW_D = 3.5
SCREW_HEAD_D = 6.5                         # counterbored from the front
BOSS_END_Y = 113.05                        # the bosses' ends, on the sheet's outer face

# -- body: free -------------------------------------------------------------------------------------
BOSS_D = 8.0
# the cover runs down the thigh, from the hip pitch's axis to past the knee's: the knee end is placed from
# the knee, so a longer thigh (the leg sheets' LINK) moves it and keeps it over the knee servo
HIP_PITCH_Z = -65.0                        # the hip pitch's axis (z, at x = -16.06)
LINK = 78.65                               # the hip pitch's axis to the knee's: the leg sheets' LINK
KNEE_Z = HIP_PITCH_Z - LINK
# the front face's corners, in order round it: about the hip (x, z), then about the knee (x, z from KNEE_Z)
HIP_END = [(-35.6, -52.61), (-16.19, -27.33), (13.67, -27.33), (32.65, -55.57), (14.89, -91.75)]   # measured
KNEE_END = [(3.09, 20.82), (2.2, 14.95), (4.77, 2.07), (-6.75, -17.76), (-25.31, -17.78), (-37.57, 3.24)]   # measured
CORNERS = HIP_END + [(x, KNEE_Z + dz) for x, dz in KNEE_END]
ROUND_R, WALL = 10.0, 3.5
BACK, PLATE_FROM, FRONT = 83.05, 119.55, 123.05   # y: the wall's back edge, the front plate
# the wall's two ends, where it opens towards the back of the leg (both by the knee): each a point on its
# inner face (x, z from KNEE_Z) and the cap's direction outwards
ENDS = (((-36.99, KNEE_Z - 10.45), (-0.894, -0.447)), ((13.03, KNEE_Z + 29.09), (0.707, 0.707)))   # measured


def face(y):
    """The plane y = const, (x, z) its coordinates; extrude(d) goes d towards -y."""
    return cq.Workplane("XZ", origin=(0, y, 0))


outline = face(FRONT).polyline(CORNERS).close()
wall = outline.offset2D(ROUND_R).extrude(FRONT - BACK).cut(face(FRONT).polyline(CORNERS).close().offset2D(ROUND_R - WALL).extrude(FRONT - BACK))
(left, ld), (right, rd) = ENDS
far = 40.0
opening = [(left[0] + far * ld[0], left[1] + far * ld[1]), left, right, (right[0] + far * rd[0], right[1] + far * rd[1])]
opening += [(opening[-1][0], -250.0), (opening[0][0], -250.0)]
wall = wall.cut(face(PLATE_FROM).polyline(opening).close().extrude(PLATE_FROM - BACK + 1))
draft = math.degrees(math.atan2(ROUND_R, FRONT - PLATE_FROM))   # the plate's edges: from R10 out at its back to the corners at the front
plate = face(PLATE_FROM).polyline(CORNERS).close().offset2D(ROUND_R).extrude(-(FRONT - PLATE_FROM), taper=draft)
shell = wall.cut(face(FRONT).rect(500, 500).extrude(FRONT - PLATE_FROM)).union(plate)

# -- interfaces, cut last -------------------------------------------------------------------------
xs, z, (d, cb), boss_end = SCREW_X, SCREW_Z, (SCREW_D, SCREW_HEAD_D), BOSS_END_Y
pts = [(x, z) for x in xs]
shell = shell.union(face(PLATE_FROM).pushPoints(pts).circle(BOSS_D / 2).extrude(PLATE_FROM - boss_end))
shell = shell.cut(face(FRONT).pushPoints(pts).circle(d / 2).extrude(FRONT - boss_end))
shell = shell.cut(face(FRONT).pushPoints(pts).circle(cb / 2).extrude(FRONT - boss_end - 2.0))

result = shell
