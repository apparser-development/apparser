from __future__ import annotations

from typing import Any

import pytest
from appwindows.geometry import Point

from apparser.movers.default import DefaultMover
from tests.utils import pyautogui_stub


@pytest.mark.parametrize("duration", ["1", object()])
def test_default_mover_rejects_invalid_duration_type(duration: Any) -> None:
    with pytest.raises(TypeError):
        DefaultMover(duration=duration)


def test_default_mover_rejects_invalid_absolute_type() -> None:
    with pytest.raises(TypeError):
        DefaultMover(absolute="yes")


def test_default_mover_rejects_negative_duration() -> None:
    with pytest.raises(ValueError):
        DefaultMover(duration=-0.1)


def test_default_mover_moves_mouse() -> None:
    mover = DefaultMover(duration=0.5)

    mover.move(Point(3, 7))

    assert pyautogui_stub.move_calls == [
        {
            "x": 3,
            "y": 7,
            "duration": 0.5,
        }
    ]
