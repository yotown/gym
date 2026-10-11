"""Flamingo skull: a small shell round the head roll's SG90, with a flamingo's bent beak and an eye
socket each side; open at the back, where the nape closes it.

A spheroid about the roll axis (so it rolls in its own outline), cut flat at the back clear of the
bracket's wall, hollowed to SKULL_WALL. Inside, a rib across it takes the SG90 by its two tabs (screws
from behind, into the rib), a window in it round the case, a notch for the cable; two bosses behind
take the nape's screws. The beak is solid: a cone out of the face, a knee, and a cone bent down.
Not in the model: the SG90's tab screws, the nape's screws (M2, self-tapping), the servo's cable.

Frame: the Duck's vendor frame (mm): x forward, z up, the head's middle at y = 0; the roll axis along x
through (ROLL_Y, ROLL_Z).
"""

import math

import cadquery as cq

from yotown.gym import shared

S = shared(__file__)
at = S.sg90_to_head

# -- interfaces -- fixed ----------------------------------------------------------------------------
ROLL_Y, ROLL_Z = S.ROLL_Y, S.ROLL_Z
TAB_FRONT_X = at((0, 0, S.SG90_TABS_Z[0]))[0]   # the SG90's tabs bear on the rib's back face here
TAB_HOLES = [at((s * S.SG90_TAB_HOLES_X, 0, 0)) for s in (1, -1)]   # (x, y, z): its tab holes
TAB_SCREW_PILOT_D = 1.6                    # M2 self-tapping, from behind through the tab into the rib
CASE_FIT = 0.3                             # the case through the rib's window, this clear all round
NAPE_SEAT_X = S.NAPE_X + S.NAPE_T    # the nape's front face, on the bosses
NAPE_SCREWS_Y = S.NAPE_SCREWS_Y         # its two screws, each side, at the roll axis's height
NAPE_SCREW_PILOT_D = 1.6
EYE_PEG_D = S.EYE_PEG_D

# -- body: free -------------------------------------------------------------------------------------
SKULL_X, SKULL_HALF_LONG, SKULL_R, SKULL_WALL = S.SKULL_X, S.SKULL_HALF_LONG, S.SKULL_R, S.SKULL_WALL
RIB_T = 3.0                                # the rib, in front of the tabs
CABLE_NOTCH_W = 5.0                        # the cable's notch, below the case's lower end
CABLE_NOTCH_DEEP = 3.0
NAPE_BOSS_LONG = 6.0                       # the nape's bosses, forward from the nape
NAPE_BOSS_W = 6.0
BEAK_ROOT_X = SKULL_X + SKULL_HALF_LONG - 10.0   # the beak: its root inside the face,
BEAK_ROOT_DOWN = 4.0                       # this far below the roll axis,
BEAK_ROOT_R = 13.0                         # this thick
BEAK_DROOP_DEG = 12.0                      # the root's run, down from level,
BEAK_ROOT_LONG = 42.0                      # this long
BEAK_KNEE_R = 8.0                          # to the knee
BEAK_BEND_DEG = 50.0                       # bent down this much more,
BEAK_TIP_LONG = 40.0                       # to the tip
BEAK_TIP_R = 2.5


def spheroid(shrink):
    """The skull's outline about the roll axis, less `shrink` all round."""
    a, b = SKULL_HALF_LONG - shrink, SKULL_R - shrink
    return cq.Workplane("XZ", origin=(SKULL_X, ROLL_Y, ROLL_Z)).ellipseArc(a, b, 0, 180, startAtCurrent=False).close().revolve(360, (-1, 0, 0), (1, 0, 0))


def cone(p, deg, long, r0, r1):
    """A cone from p (x, z at y = ROLL_Y), along x turned down by deg, this long, r0 to r1; a ball at its end."""
    d = cq.Vector(math.cos(math.radians(deg)), 0, -math.sin(math.radians(deg)))
    base = cq.Vector(p[0], ROLL_Y, p[1])
    tip = base + d * long
    body = cq.Solid.makeCone(r0, r1, long, base, d).fuse(cq.Solid.makeSphere(r1, tip, angleDegrees1=-90, angleDegrees2=90))
    return cq.Workplane(obj=body), (tip.x, tip.z)


def behind(x):
    return cq.Workplane("YZ", origin=(x, 0, 0)).rect(400, 400).extrude(-200)


outer = spheroid(0.0)
root, knee = cone((BEAK_ROOT_X, ROLL_Z - BEAK_ROOT_DOWN), BEAK_DROOP_DEG, BEAK_ROOT_LONG, BEAK_ROOT_R, BEAK_KNEE_R)
tip, _ = cone(knee, BEAK_DROOP_DEG + BEAK_BEND_DEG, BEAK_TIP_LONG, BEAK_KNEE_R, BEAK_TIP_R)
inner = spheroid(SKULL_WALL)
skull = outer.union(root).union(tip).cut(inner).cut(behind(S.NAPE_X))

# the rib across the inside, in front of the tabs; the nape's bosses from the nape forward to the wall
rib = cq.Workplane("YZ", origin=(TAB_FRONT_X, 0, 0)).rect(400, 400).extrude(RIB_T).intersect(outer)
boss_x0 = NAPE_SEAT_X
for s in (1, -1):
    y0 = s * (NAPE_SCREWS_Y - NAPE_BOSS_W / 2)
    rib = rib.union(cq.Workplane("XY", origin=(0, 0, ROLL_Z - NAPE_BOSS_W / 2))
                    .center(boss_x0 + NAPE_BOSS_LONG / 2, (y0 + s * SKULL_R) / 2).rect(NAPE_BOSS_LONG, abs(s * SKULL_R - y0))
                    .extrude(NAPE_BOSS_W).intersect(outer))
skull = skull.union(rib)

# -- interfaces, cut last -------------------------------------------------------------------------
case_lo = at((-S.SG90_LENGTH / 2, 0, 0))[2] - CASE_FIT       # the window round the case (its length hangs in z)
case_hi = at((S.SG90_LENGTH / 2, 0, 0))[2] + CASE_FIT
half_w = S.SG90_WIDTH / 2 + CASE_FIT
window = cq.Workplane("YZ", origin=(TAB_FRONT_X - 1, 0, 0)).center(ROLL_Y, (case_lo + case_hi) / 2).rect(2 * half_w, case_hi - case_lo).extrude(RIB_T + 2)
notch = cq.Workplane("YZ", origin=(TAB_FRONT_X - 1, 0, 0)).center(ROLL_Y, case_lo - CABLE_NOTCH_DEEP / 2).rect(CABLE_NOTCH_W, CABLE_NOTCH_DEEP + 0.01).extrude(RIB_T + 2)
skull = skull.cut(window).cut(notch)
skull = skull.cut(cq.Workplane("YZ", origin=(TAB_FRONT_X - 1, 0, 0)).pushPoints([(y, z) for _, y, z in TAB_HOLES]).circle(TAB_SCREW_PILOT_D / 2).extrude(RIB_T + 2))
skull = skull.cut(cq.Workplane("YZ", origin=(boss_x0 - 1, 0, 0)).pushPoints([(s * NAPE_SCREWS_Y, ROLL_Z) for s in (1, -1)])
                  .circle(NAPE_SCREW_PILOT_D / 2).extrude(NAPE_BOSS_LONG + 1))
for side, s in (("left", 1), ("right", -1)):
    x, y, z = S.eye_seat(side)
    skull = skull.cut(cq.Workplane("XZ", origin=(0, y + s, 0)).center(x, z).circle(EYE_PEG_D / 2).extrude(s * (SKULL_WALL + 3)))
result = skull
