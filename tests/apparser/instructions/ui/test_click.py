from __future__ import annotations

from typing import Any

import pytest
from appwindows.geometry import Point

from apparser.instructions.ui.click import MouseClickTo
from tests.utils import FakeUi


def test_mouse_click_to_rejects_invalid_coordinates() -> None:
    with pytest.raises(ValueError):
        MouseClickTo(object())


def test_mouse_click_to_moves_and_clicks(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []
    instruction = MouseClickTo(Point(1, 2))
    monkeypatch.setattr(
        "apparser.instructions.ui.click.MouseMove.perform",
        lambda self, ui, *args, **kwargs: calls.append("move"),
    )
    monkeypatch.setattr(
        "apparser.instructions.ui.click.MouseClick.perform",
        lambda self, *args, **kwargs: calls.append("click"),
    )

    instruction.perform(FakeUi())

    assert calls == ["move", "click"]
    assert instruction.id == 1005
