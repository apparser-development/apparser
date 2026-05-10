from __future__ import annotations

from typing import Any

import pytest
from appwindows.geometry import Point

from apparser.geometry import RelativelyPoint
from apparser.instructions.ui.mouse_move import MouseMove
from tests.utils import FakeUi, mouse_stub


@pytest.mark.parametrize("coordinates", [object(), "1"])
def test_mouse_move_rejects_invalid_coordinates(coordinates: Any) -> None:
    with pytest.raises(TypeError):
        MouseMove(coordinates)


def test_mouse_move_rejects_invalid_mover() -> None:
    with pytest.raises(TypeError):
        MouseMove(Point(1, 1), mover=object())


def test_mouse_move_moves_cursor_to_global_coordinates() -> None:
    ui = FakeUi(offset=Point(10, 20))
    instruction = MouseMove(RelativelyPoint(0.5, 0.25))

    instruction.perform(ui)

    assert mouse_stub.move_calls[0]["x"] == 60
    assert mouse_stub.move_calls[0]["y"] == 45
    assert instruction.id == 1004
