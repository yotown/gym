# Design

This note describes how the repository is organised, how its pieces depend on each other, and how
changes are versioned.

## The idea

A robot is a set of printed parts and bought parts (servos, bearings, screws, boards). In most CAD
projects each part is a separate file, and nothing connects a dimension in one part to the matching
dimension in the part it bolts to. If one changes, the other has to be found and changed by hand.

Here each printed part is a Python program, and dimensions that several parts share are defined once
and imported. This lets us use ordinary software tools on the hardware: version control, shared
libraries, builds, tests and diffs.

The same programs produce the files you print and the meshes in the simulation model, so the printed
robot and the simulated robot come from the same source.

## The pieces

The repository has the framework, and the robots and tasks built with it:

```text
src/yotown/gym/            the framework (import yotown.gym)
  interfaces.py            dimension types: BoltCircle, Screw, ScrewPattern, PinPattern, HoleGrid
  standard/                standard parts: bearings by ISO size, heat-set inserts
  bought.py                base types for bought parts: Board (outline, thickness, mounting holes)
  cli.py                   the gym command: build, check, diff
  (planned) robot.py       a robot's parts and their placements -> one assembly and its simulation model
  (planned) task/          base classes for tasks: environment and reward

vendors/<maker>/           bought parts, one folder per maker (import yotown.gym.vendors.<maker>):
                           Feetech, RobStride, ROBOTIS, Waveshare, with their sources
robots/<robot>/            one robot
  shared.py                the robot's choices: which servo, which screws, dimensions its parts share
  parts/<part>.py          one program per printed part, ending in `result`
tasks/                     tasks for the robots (planned), built on yotown.gym.task
```

A robot folder contains code, not data: `shared.py` creates the vendor objects the robot uses, and each
part program builds its shape from them.

Dependencies go one way: a part depends on its robot's `shared.py`, and `shared.py` depends on the
package. The package does not depend on anything in `robots/`.

### Bought parts are classes

A servo is not modelled in detail. It is a class that holds the dimensions the parts around it need:
its outer size, the bolt circle on its horn, its hub, its mounting tabs, each with a source (the maker's
drawing or a published model). Two robots that use the same servo use the same class. Another servo is
another class with the same attributes, so a part written for one servo can be built for another by
changing one argument.

### Shared dimensions are values

Where two parts meet (a bolt circle, a seat, a screw hole and its head), the dimension is defined once as
a value and both parts use it, so they always match. Values are not changed in place; a variant is a new
value, for example `SERVO.horn.rotated(-2.8)`.

### What a printed part weighs

A printed part is solid only in its walls, so it weighs less than its volume of plastic, and how much
less depends on its shape: a thin sheet prints almost solid, a chunky block mostly infill.
`yotown.gym.standard.materials` holds the materials' densities and `printed_mass(volume, area, settings)`,
which counts a solid skin over the part's surface and infill inside. How a part is printed is a value,
`PrintSettings(material=PLA, skin=0.8, infill=0.30)` by default: a robot's `shared.py` sets its own once
(`PRINT = PrintSettings(infill=0.2)`), and a part printed differently (a TPU sole) passes its own. A
robot's model takes each printed link's mass from it; your slicer's grams, or a print on a scale,
calibrate it.

| Material | Density, solid (g/cm³) |
|---|---|
| PLA | 1.24 (1.21 to 1.25) |
| PETG | 1.27 (1.23 to 1.29) |
| ABS | 1.04 (1.01 to 1.08) |
| TPU | 1.21 (1.10 to 1.23) |

### A part is a program

A part file starts with its parameters in two groups:

- **interfaces, fixed**: the features other parts fit. These match the original design exactly, and
  each is measured from the face it mates with.
- **body, free**: the shape between the interfaces (plates, walls, rounds). These can be changed freely.

The program then builds the body and cuts the interfaces last. A part file is a plain CadQuery script; it
uses the framework only to import shared values.

### Shared values

`robots/<robot>/shared.py` holds the values that two or more of the robot's parts must agree on: the
servo, the screws, a seat around a horn. A part reads it with `shared(__file__)`. A value used by only one
part stays in that part.

### Families

Some parts are copies or variants of another part (a left and a right side, a second copy, the same part
in another size). The design is written once and the others reuse it:

- A **twin** (same part, mirrored or moved) runs the original program and transforms the result.
- A **variant** runs the original program with its own values (`init_globals={"HOLDER": {...}}`). If a
  variant adds features, the original exposes its shape before the interfaces are cut (`blank`) and the
  interface cuts as a function (`interfaces(...)`). The variant adds its features to the blank and then
  calls `interfaces`, so its additions never cover a hole or a seat.

## Versions

The interfaces work like an API: a part printed at one version must fit the parts printed at any other
version with the same major number. Before 1.0, a breaking change raises the minor number instead
(0.1 to 0.2), so parts printed at 0.1.x fit each other. The changes are listed in `CHANGELOG.md`.

| Change | Version | Example |
|---|---|---|
| body only | patch | a thicker wall, a rounded edge added, fewer lines |
| new part, option or robot; a new interface | minor | a new variant, a second servo class |
| an interface moved, resized or removed | **major** (minor before 1.0) | a horn seat 0.2 mm wider, a different servo |

`gym diff` shows where each part gained or lost material. The reviewer compares that with the part's
interface group to decide which kind of change it is. Release notes list interface changes first.

## Workflow

```text
edit -> gym check -> gym diff -> pull request (with the diff) -> review -> merge -> release (STEP, STL)
```

- **Build**: `gym build <robot> --step --stl`. Each part is built in a separate process.
- **Test**: `gym check <robot>`. Every part must build as one valid solid. Run it for every robot you
  changed.
- **Review**: `gym diff <robot> [REV]` lists each part's added and removed material and where it is.
  Include it in the pull request.
- **Release**: a tagged version (`v0.1.0`), with interface changes listed first in `CHANGELOG.md`.

Planned: building the simulation model from the same programs, so a change can be simulated before it is
printed; small test prints of a single interface to check a fit before printing a whole part; and tasks.

## Rules for a part

1. It builds one valid solid and ends in `result`.
2. Interfaces are exact and named, in the interfaces group; everything else is in the body group.
3. Each value is written once. Values calculated from others are lower case.
4. Shared values come from `shared.py` and bought parts from `yotown.gym.vendors`. Vendor CAD only from its maker or under a licence that allows it.
5. No runtime checks inside a part; the tools check parts from outside.
