"""LeRobot humanoid knee rod, written from its STEP: one half of the rod that drives the knee from the
femur's actuator (knee_rod22, the other half, runs this program with HALF = -1). The pin and the
bearing exact, the body free.

Frame: the STEP's (mm): the rod lies in the xz plane, the halves meeting at y = 0. A pin end (a boss
and a spigot on the pin) and a bearing end (a boss seating a 15x21x4 bearing), joined by a curved
link in two layers: the inner layer stops short of the bearing, clear of it, and is pocketed; the
outer carries the bearing's boss. Screws clamp the halves; this half takes their heads.
"""

import math

import cadquery as cq

HALF = globals().get("HALF", 1)            # +1 this half (y >= 0); -1 knee_rod22

# -- interfaces: the pin and the bearing, along y -- fixed ------------------------------------------
PIN_AT, PIN_D = (-163.93, 12.26), 5.0
BEARING_AT, BEARING_OD, BEARING_WIDTH, LIP_D = (-44.91, 202.03), 21.0, 4.0, 19.0
SCREWS = [((-122.35, 141.41), 2.9), ((-126.74, 71.56), 2.9), ((-82.5, 204.95), 2.9),   # (x, z), diameter
          ((-111.43, 178.82), 3.0), ((-145.33, 41.91), 3.0)]                           # measured
HEADS_D, HEADS = 6.5, [0, 2, 4]            # the screws whose heads this half takes
INNER_T = 6.0                              # the layers
PIN_BOSS_T = 12.0
SPIGOT_D = 15.0
SPIGOT_T = 4.0

# -- body: free -------------------------------------------------------------------------------------
OUTER_T = 5.0
PIN_BOSS_D = 18.0
BEARING_BOSS_R, BEARING_CLEAR_R = 15.0, 16.0
# the outline (x, z), its points and its arcs' centres  # measured
OUTER_ARC, OUTER_R = (-50.89, 140.85), 76.47   # the long outer edge: its centre, radius


def on_outer(deg):
    """A point on the long outer edge, by its angle about the edge's centre: both layers run along
    this edge, so their points on it must be on one circle."""
    return (OUTER_ARC[0] + OUTER_R * math.cos(math.radians(deg)), OUTER_ARC[1] + OUTER_R * math.sin(math.radians(deg)))


def on_pin_boss(deg):
    """A point on the pin's boss, by its angle about the pin: the outline runs round the boss there."""
    return (PIN_AT[0] + PIN_BOSS_D / 2 * math.cos(math.radians(deg)), PIN_AT[1] + PIN_BOSS_D / 2 * math.sin(math.radians(deg)))


POCKET, NOTCH = (-59.36, 146.17), (-71.48, 159.67)    # the inner layer's pocket R42.7 and notch R25
FILLETS = ((-65.89, 202.97), (-63.84, 211.14))        # R5, either side of the bearing's clearance
BACK = [("arc", OUTER_ARC, on_outer(-155.812)), ("line", (-139.99, 78.66)), ("line", on_pin_boss(152.837)),
        ("arc", PIN_AT, on_pin_boss(-90.0)), ("arc", PIN_AT, on_pin_boss(-37.01)),
        ("line", (-114.58, 62.72)), ("line", (-84.08, 111.35))]   # the outer edge down to the pin, the inner up


def arc_mid(centre, a, b):
    """The point halfway along the shorter arc about centre from a to b."""
    m = ((a[0] + b[0]) / 2 - centre[0], (a[1] + b[1]) / 2 - centre[1])
    k = math.dist(centre, a) / math.hypot(*m)
    return (centre[0] + k * m[0], centre[1] + k * m[1])


def layer(start, path, y_from, t):
    """A side-view outline -- ("line", p), ("arc", centre, p) the shorter way, ("via", q, p) through q --
    from start, extruded t away from the rod's middle (y = 0) from y_from."""
    wp, at = cq.Workplane("XZ", origin=(0, y_from + HALF * t if HALF > 0 else y_from, 0)).moveTo(*start), start
    for kind, a, *b in path:
        end = b[0] if b else a
        wp = (wp.lineTo(*end) if kind == "line" else
              wp.threePointArc(arc_mid(a, at, end) if kind == "arc" else a, end))
        at = end
    return wp.close().extrude(t)


def across(y_from, y_to):                  # a sketch on the xz plane, extruded between two y
    lo, hi = sorted((y_from, y_to))
    return cq.Workplane("XZ", origin=(0, hi, 0)), hi - lo


# the inner layer: pocketed, notched, clear of the bearing
inner = [("line", (-62.73, 199.10)), ("arc", FILLETS[0], (-60.90, 202.75)), ("arc", BEARING_AT, (-59.33, 208.97)),
         ("arc", FILLETS[1], on_outer(100.434))] + BACK + [("arc", POCKET, (-92.82, 172.69)), ("arc", NOTCH, (-87.30, 179.03))]
rod = layer((-87.30, 179.03), inner, 0.0, INNER_T)

# the outer layer: the link out to the bearing's boss -- the inner edge straight on this half, pocketed on the other
boss_top = on_outer(84.424)
if HALF > 0:
    outer, start = [("arc", BEARING_AT, boss_top)] + BACK + [("line", (-32.21, 194.06))], (-32.21, 194.06)
else:
    b_in = (-48.67, 187.51)
    round_boss = (BEARING_AT[0] + BEARING_BOSS_R * math.cos(math.radians(-10)), BEARING_AT[1] + BEARING_BOSS_R * math.sin(math.radians(-10)))
    outer, start = [("via", round_boss, boss_top)] + BACK + [("arc", POCKET, b_in)], b_in
rod = rod.union(layer(start, outer, HALF * INNER_T, OUTER_T))

# the pin's boss and spigot, the pin through; the bearing's seat and lip
edge = HALF * (INNER_T + OUTER_T)
wp, t = across(0, HALF * PIN_BOSS_T)
rod = rod.union(wp.center(*PIN_AT).circle(PIN_BOSS_D / 2).extrude(t))
wp, t = across(HALF * PIN_BOSS_T, HALF * (PIN_BOSS_T + SPIGOT_T))
rod = rod.union(wp.center(*PIN_AT).circle(SPIGOT_D / 2).extrude(t))
wp, t = across(0, HALF * (PIN_BOSS_T + SPIGOT_T))
rod = rod.cut(wp.center(*PIN_AT).circle(PIN_D / 2).extrude(t))
wp, t = across(HALF * INNER_T, HALF * (INNER_T + BEARING_WIDTH))
rod = rod.cut(wp.center(*BEARING_AT).circle(BEARING_OD / 2).extrude(t))
wp, t = across(0, edge)
rod = rod.cut(wp.center(*BEARING_AT).circle(LIP_D / 2).extrude(t))

# the screws clamping the halves, through both layers; on this half, their heads in the outer layer
for i, (at, d) in enumerate(SCREWS):
    wp, t = across(0, edge)
    rod = rod.cut(wp.center(*at).circle(d / 2).extrude(t))
    if HALF > 0 and i in HEADS:
        wp, t = across(HALF * INNER_T, edge)
        rod = rod.cut(wp.center(*at).circle(HEADS_D / 2).extrude(t))

result = rod
