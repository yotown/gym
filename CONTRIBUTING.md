# Contributing

Thank you for helping. These programs are first versions: they build and the parts fit, but many could
be shorter and clearer. Contributions work like in any software project: open an issue or a pull
request.

## Set up

```sh
git clone https://github.com/yotown/gym && cd gym
pip install -e .            # needs CadQuery (pip or conda)
gym check so101             # every part builds one valid solid
```

## What helps most

- **Fewer lines.** A pattern instead of repeated features, a mirror instead of a second half, a
  primitive instead of a traced outline, a family instead of a near-copy.
- **Parameters that matter for a task.** Name what a task would change (an arm's reach, a gripper's
  opening, a leg's length, a wall's thickness for strength) and calculate the rest from it.
- **Shared values.** A number two parts must agree on goes in the robot's `shared.py`; a bought part's
  dimensions go in `vendors/<maker>/`, with their source.
- **The red areas** in the README's maps, where a round or a curve was simplified.
- **A new vendor part** (a servo, an actuator, a board): its dimensions and mounting features, with a
  source for each, in `vendors/<maker>/`. Makers may list their own parts; see
  [vendors/README.md](vendors/README.md) for the rules.

## The rules

1. Keep the interfaces exact. If you change one, change every part it fits in the same pull request,
   and say so: it is a breaking change (see [docs/design.md](docs/design.md), versions).
2. Give each value a name and write it once; values calculated from others are lower case.
3. Every part must still build as one valid solid and end in `result`.

## Before you open a pull request

```sh
gym check <robot>           # for every robot you touched
gym diff <robot> main       # the material each part gained and lost, and where
```

Paste the diff into the pull request and explain the change: for example the line count before and
after, any new parameters and what they do, or an interface you changed and which parts use it.

## Issues

- **Doesn't fit**: which two parts, which interface, a photo if you printed it.
- **Breaks or bends**: which part, where, under what load.
- **Prints badly**: which part, your printer and settings.

Questions: help@yotown.com.
