"""SO-101 Waveshare mounting plate, written from its STEP: the servo-driver board's plate.

A 51 x 42 plate, 4 thick, with four screw holes at its corners and a dovetailed square tenon on
top that slides into the base. Frame: the vendor's STEP (mm): the plate lies on z = 0, its centre
on the z axis; the tenon on top (z 4 .. 7.6). Symmetric about x = 0. seeedstudio_plate is this plate's
blank (plate and tenon) with its own board's holes.
"""

import cadquery as cq

PLATE = globals().get("PLATE", {})         # a sibling plate's own values (seeedstudio_plate)

# -- interfaces -- fixed ----------------------------------------------------------------------------
HOLE_D = 5.0                               # the board's corner screws
HOLE_PITCH = (37.0, 28.0)                  # x, y
PLATE_TOP_Z = 4.0                          # the base motor holder sits on it
TENON_NECK_X, TENON_NECK_Y = 15.9, 15.8    # the dovetail tenon into the holder: where it meets the plate,
TENON_NECK_H = 1.34                        # straight this high above the plate's top,
TENON_FLARE = PLATE.get("tenon_flare", 1.109)   # then flaring out this much each side  # measured
TENON_FLARE_H = PLATE.get("tenon_flare_h", 1.109)   # over this height,  # measured
TENON_TOP_Z = 7.6                          # then straight to its top

# -- body: free -------------------------------------------------------------------------------------
PLATE_X, PLATE_Y = 51.0, 42.0
PLATE_THICKNESS = 4.0
CORNER_R = 7.0                             # concentric with the holes

import math

bottom = PLATE_TOP_Z - PLATE_THICKNESS
head_x, head_y = TENON_NECK_X + 2 * TENON_FLARE, TENON_NECK_Y + 2 * TENON_FLARE
plate = (cq.Workplane("XY", origin=(0, 0, bottom)).sketch().rect(PLATE_X, PLATE_Y).vertices().fillet(CORNER_R).finalize()
         .extrude(PLATE_THICKNESS))

# the tenon: a straight neck, the dovetail's flare (planar faces), then straight to the top
flare_from = PLATE_TOP_Z + TENON_NECK_H
taper = -math.degrees(math.atan2(TENON_FLARE, TENON_FLARE_H))
tenon = (cq.Workplane("XY", origin=(0, 0, PLATE_TOP_Z)).rect(TENON_NECK_X, TENON_NECK_Y).extrude(TENON_NECK_H)
         .union(cq.Workplane("XY", origin=(0, 0, flare_from)).rect(TENON_NECK_X, TENON_NECK_Y).extrude(TENON_FLARE_H, taper=taper))
         .union(cq.Workplane("XY", origin=(0, 0, flare_from + TENON_FLARE_H)).rect(head_x, head_y).extrude(TENON_TOP_Z - flare_from - TENON_FLARE_H)))
blank = plate.union(tenon)                 # the plate and its tenon: seeedstudio_plate cuts its own holes in it

# -- interfaces, cut last -------------------------------------------------------------------------
result = blank.cut(cq.Workplane("XY", origin=(0, 0, bottom - 1)).rarray(*HOLE_PITCH, 2, 2).circle(HOLE_D / 2).extrude(PLATE_THICKNESS + 2))
