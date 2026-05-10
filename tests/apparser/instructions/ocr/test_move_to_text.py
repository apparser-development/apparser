from __future__ import annotations

import pytest
from appwindows.geometry import Point

from apparser.exceptions import TextNotFoundException
from apparser.instructions.ocr.move_to_text import MoveToText
from apparser.instructions.ocr.text_getter import GetText
from apparser.text_readers import TextData
from tests.utils import FakeTextReader, FakeUi


def test_move_to_text_finds_best_match() -> None:
    instruction = MoveToText("hello")
    texts = [
        TextData("other", [Point(0, 0)]),
        TextData("hello", [Point(1, 1)]),
    ]

    found, rating = instruction.find_text(texts)

    assert found.text == "hello"
    assert rating == 1.0


def test_move_to_text_raises_when_no_texts_exist() -> None:
    instruction = MoveToText("hello")

    with pytest.raises(TextNotFoundException):
        instruction.find_text([])


def test_move_to_text_rejects_low_similarity(monkeypatch: pytest.MonkeyPatch) -> None:
    getter = GetText()
    getter._GetText__local_answer = [
        TextData("hello", [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)])
    ]
    monkeypatch.setattr(getter, "perform", lambda ui, text_reader: None)
    instruction = MoveToText("hello", min_similarity=0.5, text_getter=getter)
    monkeypatch.setattr(
        instruction,
        "find_text",
        lambda texts: (texts[0], 0.1),
    )

    with pytest.raises(TextNotFoundException):
        instruction.perform(FakeUi(), FakeTextReader())


def test_move_to_text_moves_to_text_center(monkeypatch: pytest.MonkeyPatch) -> None:
    getter = GetText()
    getter._GetText__local_answer = [
        TextData("hello", [Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)])
    ]
    monkeypatch.setattr(getter, "perform", lambda ui, text_reader: None)
    moved_to: list[Point] = []
    monkeypatch.setattr(
        "apparser.instructions.ocr.move_to_text.MouseMove.perform",
        lambda self, ui, *args, **kwargs: moved_to.append(self._MouseMove__coordinates),
    )
    instruction = MoveToText("hello", offset=Point(1, -1), text_getter=getter)
    monkeypatch.setattr(
        instruction,
        "find_text",
        lambda texts: (texts[0], 1.0),
    )

    instruction.perform(FakeUi(), FakeTextReader())

    assert moved_to == [Point(3, 1)]
    assert instruction.id == 2001
    assert instruction.text == "hello"
