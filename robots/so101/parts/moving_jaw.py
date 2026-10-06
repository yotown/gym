"""SO-101 moving jaw: the gripper's swinging finger, written from its STEP -- interfaces exact, body free.

Frame: the vendor's (Moving_Jaw_SO101 STEP / Menagerie STL, mm). z is the gripper joint's axis,
through the origin; the jaw is a clevis about it -- the horn cheek (+z, on the servo's horn) and the
idler cheek (-z, on its idler boss) -- joined by a web at y -22..-15, and the finger runs from the
web down -y to its tip at y -81. The finger's gripping face is its flat -x side (x -8.3), with a
hooked tip (x to -12.3) for small objects. The body is symmetric about z = 0 outside the cheeks.
"""

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)                       # SO-101's shared values (../shared.py): its servo, its screws
SERVO, SERVO_SCREW = S.SERVO, S.SERVO_SCREW

# -- interfaces: from the robot model (so101.xml) and the catalogue (feetech_sts3215) -- fixed ------
HORN_INNER_Z = 17.5                        # the horn's face: the horn cheek's inner face
IDLER_INNER_Z = -18.9                      # the idler cheek's inner face
HUB_SEAT_DEPTH = 1.5                       # the horn's hub / the idler boss d6, seated in each cheek
SCREW_D = 3.2                              # M2.5 horn screws through both cheeks, heads from outside
HEAD_SEAT = 3.5                            # the screw heads' seats: this far out from each cheek's inner face
CHEEK_R = 10.0                             # the cheeks, round about the joint axis: close by the wrist follower

# -- body: free ------------------------------------------------------------------------------------
SEAT_SLOT_WIDTH = 5.0                      # each hub's seat opens to +x: the jaw slides onto the boss  # measured
BACK_X = -10.0                             # the cheeks' and the web's back
LAND_Z = 24.0                              # the cheeks' outer lands, both sides
LAND_TO_Y = 2.5                            # the lands end here # measured
WEB_Y = (-22.0, -15.0)                     # the web joining the cheeks
STEP_Z = (HORN_INNER_Z + HEAD_SEAT, IDLER_INNER_Z - HEAD_SEAT)   # the cheeks' outer faces beyond the lands: the screw heads' seats
GAP_CORNER_R = 4.2                         # the gap's corners at the web
CONTACT_X = -8.3                           # the finger's gripping face
FINGER_ROOT = (8.1, -18.3)                 # the finger's back edge, from here ...
FINGER_BEND = (3.6, -59.8)                 # ... straight to here, then in to the tip
TIP = (-7.1, -75.7)                        # the finger's back at its tip
FINGER_EDGE_R = 3.0                        # the finger's back edges
HOOK = ((CONTACT_X, -62.0), (-10.3, -62.0), (-10.3, -72.0), (-12.3, -72.0), (-12.3, -82.0), (CONTACT_X, -82.0))
# the side view (y, z >= 0), mirrored about z = 0: the finger tapers to its tip, flares into the web
SIDE = ((-81.0, 0.0), (-74.9, 5.2), (-60.0, 7.3), (-25.2, 10.8), (-22.0, 14.9), (-22.0, 18.3), (-20.1, 20.4),
        (-7.8, LAND_Z), (CHEEK_R + 1, LAND_Z))


def plan(sketch, z0=-LAND_Z, height=2 * LAND_Z):
    """A plan sketch (x, y) extruded along z."""
    return cq.Workplane("XY", origin=(0, 0, z0)).placeSketch(sketch).extrude(height)


# the plan: the round cheeks and the web, the finger, the hook at its tip
clevis = cq.Sketch().arc((0, 0), CHEEK_R, 0, 360).segment((BACK_X, WEB_Y[0]), (FINGER_ROOT[0], WEB_Y[0])).hull()
finger = (cq.Sketch().segment((CONTACT_X, WEB_Y[1]), HOOK[-1])
          .segment((FINGER_ROOT[0], WEB_Y[1]), FINGER_ROOT).segment(FINGER_ROOT, FINGER_BEND)
          .segment(FINGER_BEND, TIP).hull())
jaw = plan(clevis).union(plan(finger)).union(cq.Workplane("XY").polyline(HOOK).close().extrude(LAND_Z, both=True))

# the side view: taper the finger, flare it into the web, cap the cheeks
side = [(y, z) for y, z in SIDE] + [(y, -z) for y, z in reversed(SIDE)]
jaw = jaw.intersect(cq.Workplane("YZ", origin=(BACK_X - 3, 0, 0)).polyline(side).close().extrude(30))
# the finger's back rounded: first its corner at the bend, then its edges along the back
jaw = jaw.edges(cq.selectors.NearestToPointSelector((FINGER_BEND[0], FINGER_BEND[1], 0))).fillet(FINGER_EDGE_R)
back_mid = ((FINGER_ROOT[0] + FINGER_BEND[0]) / 2, (FINGER_ROOT[1] + FINGER_BEND[1]) / 2)
for z in (LAND_Z, -LAND_Z):
    jaw = jaw.edges(cq.selectors.NearestToPointSelector((back_mid[0], back_mid[1], z))).fillet(FINGER_EDGE_R)

# the gap between the cheeks, from the web up, where the servo's horn and idler go
gap = (cq.Workplane("YZ", origin=(BACK_X - 1, 0, 0)).center(CHEEK_R, (HORN_INNER_Z + IDLER_INNER_Z) / 2)
       .rect(2 * (CHEEK_R - WEB_Y[1]), HORN_INNER_Z - IDLER_INNER_Z).extrude(2 * CHEEK_R + 2)
       .edges("|X and <Y").fillet(GAP_CORNER_R))
jaw = jaw.cut(gap)

# the cheeks' outer faces step down beyond their lands
for z_step, z_out in ((STEP_Z[0], LAND_Z), (STEP_Z[1], -LAND_Z)):
    step = cq.Workplane("XY", origin=(0, 0, min(z_step, z_out))).center(0, LAND_TO_Y + CHEEK_R / 2)
    jaw = jaw.cut(step.rect(2 * CHEEK_R + 2, CHEEK_R).extrude(abs(z_out - z_step)))

# -- interfaces, cut last -------------------------------------------------------------------------
for z_in, inward in ((HORN_INNER_Z, 1), (IDLER_INNER_Z, -1)):      # each cheek's inner face, into it
    face = cq.Plane(origin=(0, 0, z_in), xDir=(1, 0, 0), normal=(0, 0, inward))
    seat = cq.Sketch().circle(SERVO.hub_d / 2).push([(CHEEK_R / 2, 0)]).rect(CHEEK_R, SEAT_SLOT_WIDTH).clean()
    jaw = jaw.cut(cq.Workplane(face).placeSketch(seat).extrude(HUB_SEAT_DEPTH))
    # the horn's four screws through the cheek, their heads seated in its outer face
    jaw = jaw.cut(SERVO.horn.on(cq.Workplane(face))
                  .circle(SCREW_D / 2).extrude(LAND_Z))
for z_step, z_out in ((STEP_Z[0], LAND_Z), (STEP_Z[1], -LAND_Z)):
    heads = cq.Workplane("XY", origin=(0, 0, min(z_step, z_out)))
    jaw = jaw.cut(SERVO.horn.on(heads)
                  .circle(S.HORN_SCREW_HEAD_D / 2).extrude(abs(z_out - z_step)))
# the idler's screw, through the idler cheek
jaw = jaw.cut(cq.Workplane("XY", origin=(0, 0, -LAND_Z)).circle(S.IDLER_SCREW_D / 2).extrude(LAND_Z + IDLER_INNER_Z))

result = jaw
