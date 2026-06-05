from __future__ import annotations

import pytest
from appwindows.geometry import Point, QuadPoints

from apparser.exceptions import TimeoutException
from apparser.instructions.ocr.text_getter import GetText
from apparser.instructions.ocr.wait_text import WaitText
from apparser.text_readers import TextData
from tests.utils import FakeTextReader, FakeUi


def test_wait_text_returns_when_text_is_found() -> None:
    reader = FakeTextReader(
        result=[
            TextData(
                "hello",
                QuadPoints(Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)),
            ),
        ],
    )
    instruction = WaitText("hello", interval=0, expire_time=1)

    instruction.perform(FakeUi(), reader)

    assert len(reader.images) == 1
    assert instruction.id == 2005
    assert instruction.text == "hello"


def test_wait_text_raises_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    times = iter([0.0, 2.0])
    getter = GetText()
    getter._GetText__local_answer = []

    def get_time() -> float:
        return next(times)

    def perform(ui: object, text_reader: object) -> None:
        return None

    def sleep(interval: float | int) -> None:
        return None

    monkeypatch.setattr(
        "apparser.instructions.ocr.wait_text.time.time",
        get_time,
    )
    monkeypatch.setattr(
        "apparser.instructions.ocr.wait_text.time.sleep",
        sleep,
    )
    monkeypatch.setattr(getter, "perform", perform)
    instruction = WaitText(
        "missing",
        text_getter=getter,
        interval=0,
        expire_time=1,
    )

    with pytest.raises(TimeoutException):
        instruction.perform(FakeUi(), FakeTextReader())
