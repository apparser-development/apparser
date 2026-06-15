from __future__ import annotations

from apparser.cv.events.undetected import Undetected


def test_undetected_string_representation() -> None:
    assert str(Undetected()) == "UnDetected"
