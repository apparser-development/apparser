from __future__ import annotations

from appwindows.geometry import Point

from apparser.text_readers.models.text_data import TextData


def test_text_data_is_frozen_dataclass() -> None:
    text_data = TextData("hello", [Point(1, 2), Point(3, 4)])

    assert text_data.text == "hello"
    assert text_data.coordinates == [Point(1, 2), Point(3, 4)]
