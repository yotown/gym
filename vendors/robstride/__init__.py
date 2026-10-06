"""RobStride quasi-direct-drive actuators.

Sources: RobStride's user manuals (github.com/RobStride/Product_Information): section 1.1 for the
outline and mounting dimensions (manuals 260713), section 1.3 or the electrical characteristics for the
ratings (RS00 and RS03: manual 260713; RS02 and RS05: manual 251112). Each mounting pattern here is one
the manual dimensions; holes a STEP shows but the manual does not are left out. No vendor CAD.

Not included: where each face sits along the axis. The first-hole angles are as measured in RobStride's
STEP, about the output axis; a part has to rotate them into its own frame.
"""

from __future__ import annotations

from dataclasses import dataclass

from yotown.gym.interfaces import BoltCircle, PinPattern, ScrewPattern


@dataclass(frozen=True)
class RobStride:
    """A RobStride actuator: its size, ratings, and the hole patterns on its faces. The rotor turns with
    the output; the front (output side) and back faces of the housing do not turn."""

    name: str
    diameter: float                 # the housing's largest diameter (mm)
    length: float                   # output face to back face, as the manual (mm)
    rotor_d: float                  # the turning disc on the output face: a part that holds the housing clears it
    rated_nm: float
    peak_nm: float
    reduction: float
    mass_g: float
    rotor_screws: ScrewPattern | None = None
    rotor_pins: PinPattern | None = None
    front_screws: ScrewPattern | None = None
    front_pins: PinPattern | None = None
    back_screws: ScrewPattern | None = None


RS00 = RobStride(
    "RS00", diameter=57.0, length=51.0, rotor_d=30.0, rated_nm=5.0, peak_nm=14.0, reduction=10.0, mass_g=310,
    rotor_screws=ScrewPattern(BoltCircle(27.0, 6, 30.0), "M3", 5.0),
    rotor_pins=PinPattern(BoltCircle(24.46, 3, 0.0), 3.0),
    front_screws=ScrewPattern(BoltCircle(50.0, 6, 0.0), "M3"),
    front_pins=PinPattern(BoltCircle(50.0, 2, 15.0), 3.0),
    back_screws=ScrewPattern(BoltCircle(38.0, 4, 45.0), "M3", 4.0),
)

RS02 = RobStride(
    "RS02", diameter=78.5, length=41.5, rotor_d=40.0, rated_nm=6.0, peak_nm=17.0, reduction=7.75, mass_g=405,
    rotor_screws=ScrewPattern(BoltCircle(24.0, 6, 60.0), "M4", 7.0),
    rotor_pins=PinPattern(BoltCircle(24.0, 3, 30.0), 4.0),
    front_screws=ScrewPattern(BoltCircle(73.0, 9, 33.94), "M3", 8.0),
    front_pins=PinPattern(BoltCircle(73.0, 3, 53.94), 3.0),
)

RS03 = RobStride(
    "RS03", diameter=100.5, length=54.1, rotor_d=60.0, rated_nm=20.0, peak_nm=60.0, reduction=9.0, mass_g=880,
    rotor_screws=ScrewPattern(BoltCircle(30.36, 6, 0.0), "M4", 6.0),
    rotor_pins=PinPattern(BoltCircle(30.36, 3, 90.0), 4.0),
    front_screws=ScrewPattern(BoltCircle(98.0, 8, 22.5), "M4", 8.0),
)

RS05 = RobStride(
    "RS05", diameter=46.0, length=44.0, rotor_d=32.0, rated_nm=1.6, peak_nm=5.5, reduction=7.75, mass_g=191,
    rotor_screws=ScrewPattern(BoltCircle(24.0, 6, 0.0), "M4", 3.5),
    rotor_pins=PinPattern(BoltCircle(19.0, 3, 30.0), 4.0),      # pins fitted, standing 3.0 proud of the rotor face
    front_screws=ScrewPattern(BoltCircle(41.5, 8, 22.5), "M3"),
    back_screws=ScrewPattern(BoltCircle(38.5, 4, 37.0), "M3", 10.0),
)

ALL = (RS00, RS02, RS03, RS05)
