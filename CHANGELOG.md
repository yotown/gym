# Changelog

Versions follow [semantic versioning](https://semver.org) with the rule in
[docs/design.md](docs/design.md): a change to an interface (a hole, a bolt circle, a seat, a mating
face) is a breaking change. Before 1.0, breaking changes raise the minor version (0.1 to 0.2). Each
release lists its interface changes first.

## 0.2.1

Interface changes: none. New makers and types only.

- New makers: ROBOTIS (nine DYNAMIXEL X-series servos: case, mass, gearing, stall torque and speed per
  voltage), Raspberry Pi (Pi 5, Pi 4, Zero 2 W, Camera Module 3), Adafruit (BNO085 and BNO055 IMU
  breakouts) and Waveshare (the Bus Servo Adapter (A) board).
- `yotown.gym.bought.Board`: a circuit board's outline, mounting holes (and where they sit), screw and
  thickness; and `interfaces.HoleGrid`, holes on a rectangle's corners.
- The SO-101's `waveshare_plate` takes its hole pattern from Waveshare's board, and the LeRobot
  humanoid's `torso_imu_holder` from Adafruit's BNO055 (shapes unchanged).

## 0.2.0

Interface changes: none. Import paths changed for standard parts.

- `vendors/` at the top of the repository, one folder per maker (`feetech/`, `robstride/`), each with
  a README of its parts and sources. Still imported as `yotown.gym.vendors.<maker>`. Makers can list
  their own parts: see `vendors/README.md`.
- Bearings and heat-set inserts moved to `yotown.gym.standard` (`yotown.gym.standard.bearings`,
  `yotown.gym.standard.fasteners`): they are standard sizes, not one maker's.

## 0.1.0

First release.

- Robots: SO-101 (13 printed parts), Open Duck Mini v2 (36) and the LeRobot humanoid (34), each part a
  CadQuery program, with the dimensions its parts share in the robot's `shared.py`.
- The `yotown.gym` package: dimension types (`BoltCircle`, `Screw`, `ScrewPattern`, `PinPattern`) and
  bought parts (the Feetech STS3215 servo, the RobStride RS00, RS02, RS03 and RS05 actuators, the 625,
  6702 and 6207 bearings, heat-set inserts).
- The `gym` command: `build`, `check` and `diff`.
- Error maps comparing each robot's printed parts with the upstream designs (`docs/images/`).
