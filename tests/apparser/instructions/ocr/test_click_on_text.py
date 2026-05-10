from __future__ import annotations

from appwindows.geometry import Point

from apparser.instructions.ocr.click_on_text import ClickOnText
from tests.utils import FakeTextReader, FakeUi


def test_click_on_text_moves_sleeps_and_clicks(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []
    instruction = ClickOnText("hello", offset=Point(1, 2))
    monkeypatch.setattr(
        "apparser.instructions.ocr.click_on_text.MoveToText.perform",
        lambda self, ui, ocr, *args, **kwargs: calls.append("move"),
    )
    monkeypatch.setattr(
        "apparser.instructions.ocr.click_on_text.Sleep.perform",
        lambda self, *args, **kwargs: calls.append("sleep"),
    )
    monkeypatch.setattr(
        "apparser.instructions.ocr.click_on_text.MouseClick.perform",
        lambda self, *args, **kwargs: calls.append("click"),
    )

    instruction.perform(FakeUi(), FakeTextReader())

    assert calls == ["move", "sleep", "click"]
    assert instruction.id == 2002
