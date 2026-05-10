from __future__ import annotations

import numpy
from appwindows.geometry import Point

from apparser.geometry import RelativelyPoint
from apparser.instructions.ocr.text_getter import GetText
from apparser.text_readers import TextData
from tests.utils import FakeTextReader, FakeUi


def test_text_getter_reads_and_converts_coordinates() -> None:
    screenshot = numpy.arange(300, dtype=numpy.uint8).reshape(10, 10, 3)
    reader = FakeTextReader(
        result=[
            TextData(
                "hello",
                [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)],
            )
        ]
    )
    instruction = GetText(Point(1, 1), Point(4, 3))
    ui = FakeUi(screenshot=screenshot)

    instruction.perform(ui, reader)

    assert reader.images[0].shape == (2, 3, 3)
    assert instruction.global_answer[0].coordinates[0] == Point(0, 0)
    assert instruction.local_answer[0].coordinates[0] == Point(1, 1)
    assert instruction.screenshot.shape == (2, 3, 3)


def test_text_getter_respects_cached_result() -> None:
    reader = FakeTextReader(
        result=[TextData("hello", [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)])]
    )
    instruction = GetText(
        RelativelyPoint(0, 0),
        RelativelyPoint(1, 1),
        reload_every_try=False,
    )
    ui = FakeUi()

    instruction.perform(ui, reader)
    instruction.perform(ui, reader)

    assert len(reader.images) == 1
