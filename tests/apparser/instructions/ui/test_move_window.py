from __future__ import annotations

import pytest
from appwindows.geometry import Point

from apparser.instructions.ui.move_window import WindowMove
from tests.utils import FakeUi


def test_window_move_rejects_invalid_position() -> None:
    with pytest.raises(TypeError):
        WindowMove(object())


def test_window_move_moves_window() -> None:
    ui = FakeUi()
    instruction = WindowMove(Point(3, 4))

    instruction.perform(ui)

    assert ui.window.move_calls == [Point(3, 4)]
    assert instruction.id == 1002
