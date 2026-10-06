"""Feetech bus servos.

Sources: Feetech's STS3215 2D drawing, as Waveshare publishes it for the ST3215
(https://files.waveshare.com/upload/0/08/ST3215-2D.zip), and the STS3215 STEP in TheRobotStudio's
SO-ARM100 (Apache-2.0). Where the two differ, both are given.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from yotown.gym.interfaces import BoltCircle


@dataclass(frozen=True)
class STS3215:
    """Feetech STS3215 (SO-101, Open Duck Mini v2, ...).

    Frame: about the case's centre (mm), as the SO-ARM100 STEP has it: length and width across the
    output axis, height along it; the horn on the axis's negative end, the idler boss on its positive
    end. The output axis is off the case's centre along its length, so each part places its horn.
    """

    half_length: float = 22.7       # the case with the horn discs, either side of the origin (STEP 45.4; drawing: case 45.23)
    half_width: float = 12.4        # across, either side (STEP 24.8; drawing 24.73)
    case_half_height: float = 15.9  # the case along the output axis, either side of the origin
    axis_span: tuple = (-19.4, 20.2)    # everything along the output axis: the horn end to the idler end
    horn: BoltCircle = field(default=BoltCircle(14.0, 4, 45.0))   # the horn's four holes (drawing: d2.5 on d14, 45 deg off the case)
    horn_disc_d: float = 19.2       # the horn disc (drawing; the STEP models d20)
    hub_d: float = 6.0              # the horn's hub, and the idler boss at the other end
    tab_half_pitch: float = 10.25   # the mounting tabs' screws, either side of the case's centre line

    @property
    def length(self) -> float:
        return 2 * self.half_length

    @property
    def width(self) -> float:
        return 2 * self.half_width
