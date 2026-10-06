"""SO-101 wrist camera mount, written from Menagerie's mesh (SO-ARM100 has no STEP of it): the screw
holes and the camera board's seat exact, the body free.

Frame: the mesh's (wrist_roll_follower_so101_camera_mount, mm). A bent strip: a flange down the
follower's side with two screws through it, a flat strip over the follower, and a plate rising at
the board's angle, open under the board, cut back above the opening so the board slides in from the
top; four screws through its corners.
"""

import cadquery as cq

# -- interfaces: the follower's screws, the camera board (so101.xml's wrist_camera_pcb) -- fixed ----
FLANGE_HOLE_D, FLANGE_HOLES = 2.88, [(3.09, 24.3), (-4.49, 24.3)]     # along y, (x, z)  # measured
BOARD_HOLE_D, BOARD_HOLES = 3.06, [(12.07, -50.97), (-13.96, -50.73)]  # vertical, (x, y)  # measured
BOARD_AT = (-1.01, -59.8, 46.1)            # the board's centre
BOARD_NORMAL = (0.0, 0.548, 0.837)         # out of its face, towards the lens; the plate behind it
BOARD_HOLES_4 = ((-14.51, 12.49), (-13.0, 13.0), 2.0)   # the board's four corner screws, through the plate: x, up the slope, d  # measured
BOARD_REST = -0.3                          # the standoffs' tops and the lip's edge: the board rests here; not in the model: the camera board (no mesh)  # measured
FLANGE_Y = (-27.1, -24.3)                  # the flange on the wrist follower: its faces (y)  # measured

# -- body: free -------------------------------------------------------------------------------------
FLANGE_BOTTOM = 19.4                       # the strip reaches down beside the flange to here  # measured
T = 4.6                                    # the strip  # measured
STRIP_X = (-11.8, 10.4)                    # the flange and the flat strip, across  # measured
FLAT_Y, FLAT_TOP = (-49.6, -24.3), 33.2          # measured
PLATE_X, PLATE_UP, PLATE_DOWN = (-21.6, 19.5), 19.4, 23.1   # the rising plate, about the board's centre  # measured
PLATE_W = (-7.9, -3.2)                     # its back and front, along the board's normal from the board's centre  # measured
STANDOFF_D = 4.6                           # round each corner screw  # measured
LIP = 4.6                                  # a lip along the plate's lower edge, chamfered back to the plate  # measured
WINDOW_X, WINDOW_UP, WINDOW_DOWN = (-12.0, 9.1), 8.9, 17.3  # the opening under the board  # measured
SIDE_X, SIDE_Y = (9.1, 19.5), (-48.0, -40.9)   # flats either side where the plate meets the strip  # measured


def block(x, y, z):
    return (cq.Workplane("XY").box(x[1] - x[0], y[1] - y[0], z[1] - z[0])
            .translate(((x[0] + x[1]) / 2, (y[0] + y[1]) / 2, (z[0] + z[1]) / 2)))


# the flange and the flat strip
mount = block(STRIP_X, FLANGE_Y, (FLANGE_BOTTOM, FLAT_TOP)).union(block(STRIP_X, FLAT_Y, (FLAT_TOP - T, FLAT_TOP)))

# the rising plate, in the board's plane: x across, u up the slope, w out of the board towards the lens
seat = cq.Plane(origin=BOARD_AT, xDir=(1, 0, 0), normal=BOARD_NORMAL)   # its local y runs down the slope
at = lambda x, u: (x - BOARD_AT[0], -u)              # a world x and a u up the slope, in the seat's frame
w0, w1 = PLATE_W
plate = (cq.Workplane(seat).workplane(offset=w0).center(*at(sum(PLATE_X) / 2, (PLATE_UP - PLATE_DOWN) / 2))
         .rect(PLATE_X[1] - PLATE_X[0], PLATE_UP + PLATE_DOWN).extrude(w1 - w0))
plate = plate.cut(cq.Workplane(seat).workplane(offset=w0 - 1).center(*at(sum(WINDOW_X) / 2, (WINDOW_UP - WINDOW_DOWN) / 2))
                  .rect(WINDOW_X[1] - WINDOW_X[0], WINDOW_UP + WINDOW_DOWN).extrude(w1 - w0 + 2))
hx, hu, hd = BOARD_HOLES_4
corners = [at(x, u) for x in hx for u in hu]
plate = plate.union(cq.Workplane(seat).workplane(offset=w1).pushPoints(corners).circle(STANDOFF_D / 2).extrude(BOARD_REST - w1))
plate = plate.cut(cq.Workplane(seat).workplane(offset=w0 - 1).pushPoints(corners).circle(hd / 2).extrude(BOARD_REST - w0 + 2))
# the lip: along the lower edge, up to where the board rests, chamfered back to the plate -- drawn
# square to x, in (down the slope, out of the board)
side = cq.Plane(origin=(PLATE_X[0], BOARD_AT[1], BOARD_AT[2]), xDir=seat.yDir.toTuple(), normal=(1, 0, 0))
lip = [(PLATE_DOWN, w1), (PLATE_DOWN, BOARD_REST), (PLATE_DOWN - LIP, w1)]
plate = plate.union(cq.Workplane(side).polyline(lip).close().extrude(PLATE_X[1] - PLATE_X[0]))
plate = plate.cut(block((-50, 50), (-120, 0), (0, FLAT_TOP - T)))   # trimmed flush with the strip's underside
mount = mount.union(plate)

# the flats either side of the bend, and the screw holes
for s in (1, -1):
    mount = mount.union(block(sorted(s * v for v in SIDE_X), SIDE_Y, (FLAT_TOP - T, FLAT_TOP)))
mount = mount.cut(cq.Workplane("XZ", origin=(0, FLANGE_Y[1] + 1, 0)).pushPoints(FLANGE_HOLES)
                  .circle(FLANGE_HOLE_D / 2).extrude(FLANGE_Y[1] - FLANGE_Y[0] + 2))
mount = mount.cut(cq.Workplane("XY", origin=(0, 0, FLAT_TOP - T - 1)).pushPoints(BOARD_HOLES)
                  .circle(BOARD_HOLE_D / 2).extrude(BOARD_AT[2] - FLAT_TOP + T))

result = mount
