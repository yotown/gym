"""torso13: the pelvis bar -- a bar with a hip-yaw bearing housing at each end.

Written by hand, with the author's own dimensions where they gave them. One half is modelled,
y <= 0, and mirrored about y = 0.

Two frames:
  world    x across the body, y along the bar, z up (mm).
  housing  on the housing's axis, which leans 8.089 deg toward the bar's middle and 0.2 deg
           sideways; its origin is the centre of the ring's bottom face, z up the axis.

Four values are measured, not typed (marked): the author fixed them by reference to other
geometry, not by a dimension.
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)
HIP_BEARING = S.HIP_BEARING

# -- interfaces -- fixed ----------------------------------------------------------------------------
# the hip bearing housing, at each end: the bearing on the hip yaw axis
LIP_THICKNESS = 5.0                                   # the lip over the outer race
# the yaw stop on the housing's top: a track the mating stop runs in, and the block it hits
TRACK_OD = 83.5                                       # inside it is the lip's bore; not in the model: the mating stop
TRACK_DEPTH = 3.0
STOP_ARC = 60.0                                       # degrees, centred on the housing's +x; not in the model: the hip yaw's range
# the bolts that hold the next link to the housing, from underneath
BOLT_HOLE_D = 3.8
BOLT_COUNT = 8
BOLT_FIRST_DEG = 22.967                               # measured
# on the centre line: a d8 bore at 60 deg
PIN_D = 8.0
PIN_ANGLE = 60.0                                      # up from the bar's bottom, leaning outward
PIN_AT_Y = -35.0                                      # where its axis leaves the bar's bottom
BAR_BOTTOM_Z = -93.0                                  # on the upper body; the pin's bore leaves it
HOUSING_OD = 102.0                                    # against torso22

# -- body: free -------------------------------------------------------------------------------------
LIP_ID = 66.0                                         # the lip's bore: on the outer race only, keep it between the races (d < 72)
UNDERCUT = 6.0                                        # the bar is trimmed this far below the ring
STOP_HEIGHT = 2.0
BOLT_DEPTH = 15.0                                     # from the undercut face
SLOT_WIDTH = 4.0                                      # the slot on the centre line, ending in the pin's bore
BAR_WIDTH = 100.0
BAR_HALF_LENGTH = 130.0                               # the author's 205 - 75
BAR_TOP_Z = -56.966                                   # measured: drawn to z -55 (38 tall), its top cut down to here
STOP_FILLET = 2.0

housing = cq.Plane(origin=S.HIP_HOUSING_ORIGIN, xDir=(1, 0, 0), normal=(0, 0, 1)).rotated((*S.HIP_HOUSING_TILT, 0))
housing_top = HIP_BEARING.width + LIP_THICKNESS


def on_housing(z=0.0):
    """A workplane square to the housing's axis, `z` up it from the ring's bottom."""
    return cq.Workplane(housing).workplane(offset=z)


def annular_sector(wp, inner_d, outer_d, start_deg, end_deg):
    """The ring between two diameters from one angle to another, as a closed sketch."""
    ri, ro = inner_d / 2, outer_d / 2
    a0, a1 = math.radians(start_deg), math.radians(end_deg)
    am = (a0 + a1) / 2
    at = lambda r, a: (r * math.cos(a), r * math.sin(a))  # noqa: E731
    return (wp.moveTo(*at(ri, a0)).lineTo(*at(ro, a0)).threePointArc(at(ro, am), at(ro, a1))
            .lineTo(*at(ri, a1)).threePointArc(at(ri, am), at(ri, a0)).close())


# The bar: one half, cleared inside the housing and trimmed square to the housing below it
bar = (cq.Workplane("XY").workplane(offset=BAR_BOTTOM_Z).center(0, -BAR_HALF_LENGTH / 2)
       .rect(BAR_WIDTH, BAR_HALF_LENGTH).extrude(BAR_TOP_Z - BAR_BOTTOM_Z))
bar = bar.cut(on_housing(-500).circle(HOUSING_OD / 2).extrude(1000))
bar = bar.cut(on_housing(-UNDERCUT).rect(1000, 1000).extrude(-100))

# The housing: the bearing's seat from below, the lip on top
ring = (on_housing().circle(HOUSING_OD / 2).extrude(housing_top)
        .cut(on_housing().circle(HIP_BEARING.od / 2).extrude(HIP_BEARING.width))
        .cut(on_housing().circle(LIP_ID / 2).extrude(housing_top)))
half = bar.union(ring)

# The yaw stop: the track all round but the stop's arc, and the stop block raised on that arc
half_arc = STOP_ARC / 2
half = half.cut(annular_sector(on_housing(housing_top), LIP_ID, TRACK_OD, half_arc, 360 - half_arc).extrude(-TRACK_DEPTH))
half = half.union(annular_sector(on_housing(housing_top), LIP_ID, HOUSING_OD, -half_arc, half_arc).extrude(STOP_HEIGHT))
r_in = LIP_ID / 2
corners = [housing.toWorldCoords((r_in * math.cos(math.radians(a)), r_in * math.sin(math.radians(a)), housing_top))
           for a in (-half_arc, half_arc)]
half = half.newObject([min(half.edges().vals(), key=lambda e: e.distance(cq.Vertex.makeVertex(*c.toTuple())))
                       for c in corners]).fillet(STOP_FILLET)

# Bolt holes, from the undercut face up into the ring
half = half.cut(on_housing(-UNDERCUT).polarArray(S.HIP_HOUSING_BOLT_CIRCLE_D / 2, BOLT_FIRST_DEG, 360, BOLT_COUNT)
                .circle(BOLT_HOLE_D / 2).extrude(BOLT_DEPTH))

# The pin bore and the slot, on the centre line
t = math.radians(PIN_ANGLE)
along_pin = (0, -math.cos(t), math.sin(t))
half = half.cut(cq.Workplane(cq.Plane(origin=(0, PIN_AT_Y, BAR_BOTTOM_Z), xDir=(1, 0, 0), normal=along_pin))
                .workplane(offset=-50).circle(PIN_D / 2).extrude(150))
run = (BAR_TOP_Z - BAR_BOTTOM_Z) / math.tan(t)
half = half.cut(cq.Workplane("YZ").workplane(offset=-SLOT_WIDTH / 2)
                .polyline([(PIN_AT_Y, BAR_BOTTOM_Z), (PIN_AT_Y - run, BAR_TOP_Z),
                           (-BAR_HALF_LENGTH, BAR_TOP_Z), (-BAR_HALF_LENGTH, BAR_BOTTOM_Z)]).close()
                .extrude(SLOT_WIDTH))

result = half.mirror("XZ", union=True)
