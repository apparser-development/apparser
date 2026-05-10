from __future__ import annotations

from apparser.cv.events.undetected import UnDetected


def test_undetected_string_representation() -> None:
    assert str(UnDetected()) == "UnDetected"
