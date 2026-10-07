"""LeRobot humanoid IMU holder, written from its STEP: a 3 mm plate that carries the IMU board, on
four standoffs at the base board's screw grid (as torso_can_holder_2's).

Frame: the STEP's (mm). The plate lies on z -145.7; the IMU's holes are centred on the z axis.
The plate between the standoffs is body: a pad under the IMU, a bar across +y with a leg to each
+y standoff, and an arm to each -y standoff. Not drawn: the R3 blends where they meet."""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)

# -- interfaces -- fixed ----------------------------------------------------------------------------
STANDOFF_BORE_D = 3.0
STANDOFF_D, STANDOFF_TOP_Z = 5.82, -132.17   # the board sits on them; not in the model: the board
IMU_HOLE_D, IMU_PITCH = 2.0, S.IMU.holes.pitch       # 0.8 x 0.6 in: the IMU board's holes (its own: d2.5)
PLATE_TOP_Z = -142.7                                  # the IMU's seat; not in the model: the IMU

# -- body: free -------------------------------------------------------------------------------------
PLATE_T = 3.0                              # down from the IMU's seat
PAD = (25.4, (-10.16, 3.0))                # its width, its y from .. to
BAR_Y = (3.0, 10.16)                       # across +y, standoff to standoff
ARMS = {(1, -1): ((12.7, -8.15), 6.0),      # the -y standoffs' arms: where each meets the pad, its width;
        (-1, -1): ((-6.25, -10.16), 5.82)}  # the +x one's standoff is as wide as its arm  # measured

BOTTOM_Z = PLATE_TOP_Z - PLATE_T
bx, by = S.TORSO_BOARD_PITCH[0] / 2, S.TORSO_BOARD_PITCH[1] / 2
standoff = {(sx, sy): (S.TORSO_BOARD_AT[0] + sx * bx, S.TORSO_BOARD_AT[1] + sy * by) for sx in (1, -1) for sy in (1, -1)}

(y0, y1) = PAD[1]
x_lo, x_hi = standoff[(-1, 1)][0] - STANDOFF_D / 2, standoff[(1, 1)][0] + STANDOFF_D / 2
plate = (cq.Sketch()
         .push([(0, (y0 + y1) / 2)]).rect(PAD[0], y1 - y0)
         .push([((x_lo + x_hi) / 2, sum(BAR_Y) / 2)]).rect(x_hi - x_lo, BAR_Y[1] - BAR_Y[0]))
for sx in (1, -1):
    x, y = standoff[(sx, 1)]
    plate = plate.push([(x, (BAR_Y[0] + y) / 2)]).rect(STANDOFF_D, y - BAR_Y[0])
for key, ((ix, iy), width) in ARMS.items():
    x, y = standoff[key]
    length = math.hypot(x - ix, y - iy)
    angle = math.degrees(math.atan2(y - iy, x - ix))
    plate = plate.push([((x + ix) / 2, (y + iy) / 2)]).slot(length, width, angle=angle)

holder = cq.Workplane("XY", origin=(0, 0, BOTTOM_Z)).placeSketch(plate.reset().clean()).extrude(PLATE_T)
for key, at in standoff.items():
    d = ARMS[key][1] if key == (1, -1) else STANDOFF_D
    holder = holder.union(cq.Workplane("XY", origin=(0, 0, BOTTOM_Z)).center(*at).circle(d / 2).extrude(STANDOFF_TOP_Z - BOTTOM_Z))
holder = holder.cut(cq.Workplane("XY", origin=(0, 0, BOTTOM_Z)).pushPoints(list(standoff.values()))
                    .circle(STANDOFF_BORE_D / 2).extrude(STANDOFF_TOP_Z - BOTTOM_Z))
result = holder.cut(cq.Workplane("XY", origin=(0, 0, BOTTOM_Z)).rarray(*IMU_PITCH, 2, 2).circle(IMU_HOLE_D / 2).extrude(PLATE_T))
