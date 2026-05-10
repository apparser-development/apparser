from __future__ import annotations

from appwindows.geometry import Point

from apparser.instructions.ocr.print_all_text import PrintAllText
from apparser.instructions.ocr.text_getter import GetText
from apparser.text_readers import TextData
from tests.utils import FakeTextReader, FakeUi


def test_print_all_text_prints_each_entry(monkeypatch: pytest.MonkeyPatch) -> None:
    getter = GetText()
    getter._GetText__local_answer = [
        TextData("hello", [Point(1, 2), Point(3, 4)]),
    ]
    printed: list[str] = []
    monkeypatch.setattr(getter, "perform", lambda ui, text_reader: None)
    monkeypatch.setattr("builtins.print", lambda value: printed.append(value))
    instruction = PrintAllText(text_getter=getter)

    instruction.perform(FakeUi(), FakeTextReader())

    assert printed == ['text: "hello", coordinates: Point(x = 1, y = 2) Point(x = 3, y = 4) ']
    assert instruction.id == 2003
