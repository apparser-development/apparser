from __future__ import annotations

from apparser.cv.events.detected import Detected


def test_detected_string_representation() -> None:
    assert str(Detected()) == "Detected"
