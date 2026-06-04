from __future__ import annotations

from apparser.instructions.ui.to_window import WindowToBackground, WindowToForeground
from tests.utils import FakeUi


def test_window_to_background_moves_window_back() -> None:
    ui = FakeUi()
    instruction = WindowToBackground()

    instruction.perform(ui)

    assert ui.window.to_background_calls == 1
    assert instruction.id == 1001


def test_window_to_foreground_brings_window_forward() -> None:
    ui = FakeUi()
    instruction = WindowToForeground()

    instruction.perform(ui)

    assert ui.window.to_foreground_calls == 1
    assert instruction.id == 1000
