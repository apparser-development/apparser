from __future__ import annotations

from apparser.cv.events.resized import Resized


def test_resized_string_representation() -> None:
    assert str(Resized()) == "Resized"
