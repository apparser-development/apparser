from __future__ import annotations

from unittest.mock import Mock

import numpy
from appwindows.geometry import Point, QuadPoints

from apparser.instructions.ocr.plot_text import PlotAllText, _Painter
from apparser.instructions.ocr.text_getter import GetText
from apparser.text_readers import TextData
from tests.utils import FakeTextReader, FakeUi


def test_painter_draws_rectangle_and_text() -> None:
    draw = Mock()
    painter = _Painter(draw, (255, 255, 255, 255))
    data = TextData("hello", QuadPoints(Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)), )

    painter.draw([data])

    draw.rectangle.assert_called_once()
    draw.text.assert_called_once()


def test_plot_all_text_draws_and_shows_image(monkeypatch: pytest.MonkeyPatch) -> None:
    getter = GetText()
    getter._GetText__global_answer = [
        TextData("hello", QuadPoints(Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)), )
    ]
    getter._GetText__screenshot = numpy.zeros((4, 4, 3), dtype=numpy.uint8)
    monkeypatch.setattr(getter, "perform", lambda ui, text_reader: None)
    painter_calls: list[list[TextData]] = []
    shown: list[bool] = []
    monkeypatch.setattr("apparser.instructions.ocr.plot_text._Painter.draw", lambda self, texts: painter_calls.append(texts))
    monkeypatch.setattr("PIL.Image.Image.show", lambda self: shown.append(True))
    instruction = PlotAllText(text_getter=getter)

    instruction.perform(FakeUi(), FakeTextReader())

    assert painter_calls == [getter.local_answer]
    assert shown == [True]
    assert instruction.id == 2004
