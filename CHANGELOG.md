# Changelog

Versions follow [semantic versioning](https://semver.org) with the rule in
[docs/design.md](docs/design.md): a change to an interface (a hole, a bolt circle, a seat, a mating
face) is a breaking change. Before 1.0, breaking changes raise the minor version (0.1 to 0.2). Each
release lists its interface changes first.

## 0.1.0

First release.

- Robots: SO-101 (13 printed parts), Open Duck Mini v2 (36) and the LeRobot humanoid (34), each part a
  CadQuery program, with the dimensions its parts share in the robot's `shared.py`.
- The `yotown.gym` package: dimension types (`BoltCircle`, `Screw`, `ScrewPattern`, `PinPattern`) and
  bought parts (the Feetech STS3215 servo, the RobStride RS00, RS02, RS03 and RS05 actuators, the 625,
  6702 and 6207 bearings, heat-set inserts).
- The `gym` command: `build`, `check` and `diff`.
- Error maps comparing each robot's printed parts with the upstream designs (`docs/images/`).
