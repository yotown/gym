# Code quality

What makes a part program good: the bar every printed part in this repository is held to, and how it
is measured. A program can make the right shape and still be poor code: a record of coordinates
nobody can change. Here a part is done when it is right, when it fits the parts around it, and when an
engineer can read it and change it.

## The bar

A part program is done when:

1. **It builds one valid solid** (one per body, for a part printed as several), every time, from a
   fresh Python.
2. **Its interfaces are exact.** Every face that meets another part (a servo pocket, a bolt
   circle, a bearing seat, a horn spline) is a named parameter, read from the shared definitions
   (`yotown.gym.interfaces`, `vendors/`, `standard/`) rather than typed again. Interfaces are the
   contract between parts, like an API: they are pinned, and everything between them is free.
3. **It reads like an engineer wrote it.** The measures below.
4. **It survives an edit.** Change a named parameter and the part still builds, as valid solids.

Matching someone else's shape to the last tenth of a millimetre is not part of the bar. A round, a
draft or a rib that the shape needs is fine, written as a named feature.

## Quality for a task

The bar above holds for any part. But the programs exist so that the body can change with the task:
a longer leg for a jump, a wider stance for a push, a stronger motor at the knee, a camera moved to
the wrist. The body and its controller are trained together, so the body must be as easy to change as
the controller. Which changes matter depends on the task, so good code depends on the task too.

A task names the body changes it searches: link lengths, joint offsets, a motor chosen from the
catalogue, where a sensor sits, each with the range the task allows. Its parts are then held to
three more things:

1. **Every change the task searches is a named parameter.** A link length is one number in one
   place, not a position repeated in three sketches. The measure: the share of the task's changes
   the programs expose (target: all of them).
2. **A change carries to every part it touches.** Lengthening a shin moves the knee's mount and
   the ankle's mount; swapping a motor changes its pocket, its bolt circle and the horn it drives.
   Parts that meet read the shared dimension from one place, so no part is left behind. The measure:
   over the task's changes, the robot still assembles: every interface still meets its mate.
3. **It survives the task's whole range.** The edit test above, run over the range the task gives
   each change. A part that breaks inside that range cannot be searched there.

The same programs build the printed parts and the simulation model, so a body the search finds is
one that can be printed. A part that meets the general bar but hides the task's changes in fixed
geometry is good code for a drawing and poor code for this framework.

## The measures

Each is defined on the program text, except the edit test, which builds it.

| Group | Measure | What it counts | Target |
|---|---|---|---|
| Compact | lines per feature | code lines (no blanks, no comments) per modelling operation | ≤ 2.5 |
| Parametric | inline ratio | numbers written inside feature code, as a share of all numbers (inline + named) | ≤ 0.42 |
| | measured numbers | numbers finer than the part's own drawing precision (the precision its interface dimensions are given in): readings, not typed values | 0 |
| | reuse | uses of named parameters per parameter | ≥ 1.75 |
| Vocabulary | primitive share | circles, arcs, rectangles, slots and polygons among the sketch elements, rather than point-by-point lines | ≥ 0.95 |
| | pattern capture | repeated equal circles written as a pattern rather than one by one | ≥ 0.95 |
| | indexed names | parameter names carrying an index (`hole_3`, `r_12`) | 0 |
| Editable | edit pass | of the named parameters, the share that pass the edit test | ≥ 0.9 |

**Features** are what an engineer counts in a feature tree: extrude, revolve, cut, hole, fillet,
chamfer, shell, loft, sweep, union, intersect, mirror and the patterns (`rarray`, `polarArray`,
`pushPoints`).

**Inline numbers** are not all bad. Positions often read best where they are used; sizes should be
named. The target allows for that: it is the median of the hand-written programs we accepted.

**The edit test** separates a program from a record of geometry. A record breaks when you touch it: a
wall goes negative, a fillet fails, a hole leaves its boss. A program carries its intent in its
parameters and relations, so it bends.

## Where the targets come from

Every target is the median of the same measures over the hand-written programs we accepted as good
(65 programs for the text measures, 15 built for the edit test). So "engineer-like" means "at least as
good as what we already accepted", not a number chosen in advance. When the accepted set grows, the
targets are measured again.

A part that meets every target is not finished by that fact alone. The measures catch the common ways
code goes wrong; reading it still decides.

## What it looks like

Poor, a record of a shape:

```python
part = (cq.Workplane("XY")
        .moveTo(-21.0, -10.1).lineTo(-19.1, -12.0).lineTo(19.1, -12.0).lineTo(21.0, -10.1)
        .lineTo(21.0, 10.1).lineTo(19.1, 12.0).lineTo(-19.1, 12.0).lineTo(-21.0, 10.1)
        .close().extrude(5.0)
        .faces(">Z").workplane()
        .moveTo(-15.0, -6.0).circle(1.6).cutThruAll()
        .moveTo(15.0, -6.0).circle(1.6).cutThruAll()
        .moveTo(-15.0, 6.0).circle(1.6).cutThruAll()
        .moveTo(15.0, 6.0).circle(1.6).cutThruAll())
```

Good, the same plate as a program:

```python
from yotown.gym.interfaces import HoleGrid

width, depth, thickness = 42.0, 24.0, 5.0
corner_chamfer = 1.9
mount = HoleGrid(pitch=(30.0, 12.0), hole_d=3.2)    # the interface: shared with the mating part

plate = (cq.Workplane("XY")
         .rect(width, depth).extrude(thickness)
         .edges("|Z").chamfer(corner_chamfer)
         .faces(">Z").workplane())
plate = mount.on(plate).hole(mount.hole_d)
```

Both build the same solid. The second says what each number is, takes its holes from the part it
mates with, and still builds when `width` or the pitch changes. Measured:

| | lines per feature | inline ratio | reuse | primitive share | pattern capture | targets met |
|---|---|---|---|---|---|---|
| poor | 2.2 | 1.0 | 0 | 0.36 | 0 | 3 of 7 |
| good | 3.7 | 0 | 1.0 | 1.0 | 1.0 | 5 of 7 |

The good one misses two targets, and that is expected: a part this small has few features to spread
its parameter lines over, and each parameter is used once. The measures are for whole parts; on a
toy, read them as direction, not verdict.
