from __future__ import annotations

from apparser.cv.events.moved import Moved


def test_moved_string_representation() -> None:
    assert str(Moved()) == "Moved"
