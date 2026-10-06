"""LeRobot humanoid tibia rod (the long one), written from its STEP: the two pins exact, the body free.
tibias2_rod_small is the same rod with its own dimensions: it runs this program with its ROD.

An angle bar along z between two pins: its legs join at a rounded heel; at each pin a solid tab, its
far corner round about the pin. Frame: the STEP's (mm)."""

import cadquery as cq

ROD = globals().get("ROD", {})            # tibias2_rod_small's values

# -- interfaces -- fixed ----------------------------------------------------------------------------
PIN_AT = ROD.get("pin_at", (-50.0, 24.0))   # the pins along z (x, y)
PIN_PITCH = ROD.get("pin_pitch", 148.0)    # pin to pin, down z from z = 0
PIN_D = 5.0

# -- body: free -------------------------------------------------------------------------------------
HEEL = ROD.get("heel", (-1, -1))           # the heel's corner from the pin: towards -x, -y
SIDE = ROD.get("side", (14.0, 14.0))       # the section (x, y)
LEG = ROD.get("leg", (4.0, 4.0))           # the legs' thickness across x, across y
HEEL_R, TIP_R, TAB_R = 5.0, 2.5, 5.0       # the heel, the legs' tips, the tab's corner about the pin
TAB_T = 5.0                                # each tab, centred on its pin

(px, py), (sx, sy) = PIN_AT, HEEL
(W, H), (LU, LV) = SIDE, LEG
x0, y0 = px + sx * (W - TAB_R), py + sy * (H - TAB_R)   # the heel's corner


def P(u, v):                               # u along x, v along y, inwards from the heel's corner
    return (x0 - sx * u, y0 - sy * v)


def corner(cu, cv, r, du, dv):             # the point on a round corner (centre cu, cv) halfway round
    return P(cu + du * r * 0.7071, cv + dv * r * 0.7071)


def outline(tab):
    wp = cq.Workplane("XY").moveTo(*P(0, HEEL_R)).lineTo(*P(0, H))
    if tab:
        wp = wp.lineTo(*P(W - TAB_R, H)).threePointArc(corner(W - TAB_R, H - TAB_R, TAB_R, 1, 1), P(W, H - TAB_R))
    else:
        wp = (wp.lineTo(*P(LU - TIP_R, H)).threePointArc(corner(LU - TIP_R, H - TIP_R, TIP_R, 1, 1), P(LU, H - TIP_R))
              .lineTo(*P(LU, LV)).lineTo(*P(W - TIP_R, LV))
              .threePointArc(corner(W - TIP_R, LV - TIP_R, TIP_R, 1, 1), P(W, LV - TIP_R)))
    return (wp.lineTo(*P(W, 0)).lineTo(*P(HEEL_R, 0))
            .threePointArc(corner(HEEL_R, HEEL_R, HEEL_R, -1, -1), P(0, HEEL_R)).close())


pitch = PIN_PITCH
rod = outline(False).extrude(-(pitch - TAB_T)).translate((0, 0, -TAB_T / 2))
for z in (0.0, -pitch):
    tab = cq.Workplane("XY").add(outline(True).extrude(TAB_T).val()).translate((0, 0, z - TAB_T / 2))
    rod = rod.union(tab).cut(cq.Workplane("XY").center(px, py).circle(PIN_D / 2).extrude(TAB_T).translate((0, 0, z - TAB_T / 2)))

result = rod
