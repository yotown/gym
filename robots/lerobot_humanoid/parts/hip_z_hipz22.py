"""LeRobot humanoid hip yaw link (hip_z 22), written from its STEP: a 25 mm plate around a 35x72x17
bearing, two bolt circles about it, and an axle pin standing on the plate.

Frame: on the plate's bottom face, z up its thickness, the origin on the bearing's axis; x points
away from the plate's lobe. The plate is tilted in the STEP's frame, so the frame is measured;
everything else is an offset in it. The plate's outline is two circles -- about the bearing, and
the lobe's -- joined by R100 blends; a slot runs into the lobe's far end. Under the lobe, a 5 mm
recess from the bottom face."""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # the LeRobot humanoid's shared values (../shared.py)
HIP_BEARING, M3 = S.HIP_BEARING, S.M3

# -- frame: measured --------------------------------------------------------------------------------
ORIGIN = (-18.4524848506, 28.111297708777, -0.262171570133)        # measured

# -- interfaces -- fixed ----------------------------------------------------------------------------
SEAT_DEPTH = 22.0                          # the 35x72x17 bearing, from the bottom face
BOLT_CIRCLE_D = 90.0
SCREW_D = 3.8                                   # on a 45 deg pitch from FIRST_DEG; none at the slot's side
SCREW_DEPTH = 15.0                              # not in the model: those screws
SCREW_FIRST_DEG, SCREW_SKIPPED = 22.93, (4,)    # measured
CBORE_SCREW_D = 3.9                             # M3.5, counterbored from the top
CBORE_D, CBORE_FROM_Z = 7.5, 19.0               # not in the model: the M3.5 screws
CBORE_DEG = (142.33, 157.11)                    # and their mirrors about x  # measured
TAP_D, TAP_CIRCLE_D, TAP_DEG = 3.1, 86.0, (180.0, 350.0)   # M3, from the bottom
TAP_DEPTH = 17.5                                # not in the model: the M3 screws
PIN_D = 5.0                                     # the axle pin on the 180 deg tap's axis

# -- body: free -------------------------------------------------------------------------------------
BORE_D = 66.0                                   # above the seat, inside the outer race
PIN_TOP_Z, CONE_BASE_D = 35.0, 15.0             # the pin's top; it stands on a 45 deg cone
THICKNESS = 25.0
DISC_R = 51.0                                   # about the bearing
LOBE_AT = (-14.0, 0.0)
LOBE_R = 45.0
BLEND_R = 100.0                                 # the outline's concave blends, disc to lobe
SLOT_END_AT = (-54.5, 0.0)                 # the slot ends in this hole
SLOT_END_R = 3.0
SLOT_W = 4.0                               # its direction, and its centre line's offset at the end  # measured
SLOT_DEG = -9.8
SLOT_OFFSET = -0.34
RECESS_DEPTH = 5.0                              # under the lobe, from the bottom face, up to the slot
RECESS_INNER_AT = (-15.951, 0.0)           # measured
RECESS_INNER_R = 35.549
RECESS_OUTER_R = 43.5                           # about the lobe: leaves a rib on the outline
RECESS_END = ((-30.830, 35.306), (-32.206, 41.152))         # its straight end  # measured
RECESS_CORNER_R = 3.5


def polar(r, deg, at=(0.0, 0.0)):
    return (at[0] + r * math.cos(math.radians(deg)), at[1] + r * math.sin(math.radians(deg)))


def blended_circles(wp, r1, at2, r2, rb):
    """Two circles -- r1 about the origin, r2 about a point on the x axis -- joined by blends of
    radius rb tangent to both, as one closed outline."""
    c2 = at2[0]
    cx = (c2 ** 2 - (r2 + rb) ** 2 + (r1 + rb) ** 2) / (2 * c2)
    cy = math.sqrt((r1 + rb) ** 2 - cx ** 2)
    pts = {}
    for s in (1, -1):
        c = (cx, s * cy)
        t1 = (c[0] * r1 / (r1 + rb), c[1] * r1 / (r1 + rb))
        t2 = (c2 + (c[0] - c2) * r2 / (r2 + rb), c[1] * r2 / (r2 + rb))
        m = ((t1[0] + t2[0]) / 2 - c[0], (t1[1] + t2[1]) / 2 - c[1])
        k = rb / math.hypot(*m)
        pts[s] = (t1, t2, (c[0] + m[0] * k, c[1] + m[1] * k))
    (t1u, t2u, mu), (t1l, t2l, ml) = pts[1], pts[-1]
    far1, far2 = (r1, 0.0) if c2 < 0 else (-r1, 0.0), (c2 - r2, 0.0) if c2 < 0 else (c2 + r2, 0.0)
    return (wp.moveTo(*t1l).threePointArc(far1, t1u).threePointArc(mu, t2u)
            .threePointArc(far2, t2l).threePointArc(ml, t1l).close())


bottom = cq.Workplane(cq.Plane(origin=ORIGIN, xDir=S.HIPZ_X_DIR, normal=S.HIPZ_NORMAL))

# the outline: the disc and the lobe, blended
plate = blended_circles(bottom, DISC_R, LOBE_AT, LOBE_R, BLEND_R).extrude(THICKNESS)

# the slot into the lobe's end, and its end hole
d = math.radians(SLOT_DEG)
slot_centre = (SLOT_END_AT[0] - 10 * math.cos(d), SLOT_END_AT[1] + SLOT_OFFSET - 10 * math.sin(d))
slot = cq.Sketch().push([slot_centre]).rect(20, SLOT_W, angle=SLOT_DEG).reset().push([SLOT_END_AT]).circle(SLOT_END_R)
plate = plate.cut(bottom.placeSketch(slot).extrude(THICKNESS))

# the recess under the lobe: between two arcs, from the slot to its straight end
(ax, ay), (bx, by) = RECESS_END
ux, uy = ax - bx, ay - by
wedge = [(-70.0, SLOT_END_AT[1] + SLOT_OFFSET + SLOT_W / 2 - 15.5 * math.tan(d)), (-40.0, 0.0),
         (ax + 2 * ux, ay + 2 * uy), (bx - ux, by - uy), (-70.0, 45.0)]
recess = (cq.Sketch().push([LOBE_AT]).circle(RECESS_OUTER_R).reset()
          .push([RECESS_INNER_AT]).circle(RECESS_INNER_R, mode="s").reset()
          .polygon(wedge + [wedge[0]], mode="i").reset()
          .vertices(cq.selectors.NearestToPointSelector((ax + 0.5, ay - 3.5, 0))).fillet(RECESS_CORNER_R))
plate = plate.cut(bottom.placeSketch(recess).extrude(RECESS_DEPTH))

# the bearing
plate = plate.cut(bottom.circle(HIP_BEARING.od / 2).extrude(SEAT_DEPTH))
plate = plate.cut(bottom.circle(BORE_D / 2).extrude(THICKNESS))

# the axle pin, on a 45 deg cone, on the plate's top
top = bottom.workplane(offset=THICKNESS)
pin_at = polar(TAP_CIRCLE_D / 2, TAP_DEG[0])
cone_h = (CONE_BASE_D - PIN_D) / 2
cone = cq.Solid.makeCone(CONE_BASE_D / 2, PIN_D / 2, cone_h, top.plane.toWorldCoords(pin_at), top.plane.zDir)
plate = plate.union(cq.Workplane().add(cone))
plate = plate.union(top.center(*pin_at).circle(PIN_D / 2).extrude(PIN_TOP_Z - THICKNESS))

# the screws: from the bottom, a 45 deg pitch less the skipped place; the counterbored ones from the top
screws = [polar(BOLT_CIRCLE_D / 2, SCREW_FIRST_DEG + 45 * k) for k in range(8) if k not in SCREW_SKIPPED]
plate = plate.cut(bottom.pushPoints(screws).circle(SCREW_D / 2).extrude(SCREW_DEPTH))
cbores = [polar(BOLT_CIRCLE_D / 2, s * a) for a in CBORE_DEG for s in (1, -1)]
plate = plate.cut(bottom.pushPoints(cbores).circle(CBORE_SCREW_D / 2).extrude(THICKNESS))
plate = plate.cut(bottom.workplane(offset=CBORE_FROM_Z).pushPoints(cbores).circle(CBORE_D / 2).extrude(THICKNESS))
taps = [polar(TAP_CIRCLE_D / 2, a) for a in TAP_DEG]
result = plate.cut(bottom.pushPoints(taps).circle(TAP_D / 2).extrude(TAP_DEPTH))
