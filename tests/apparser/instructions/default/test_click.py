from __future__ import annotations

import pytest

from apparser.instructions.default.click import MouseClick
from apparser.key_codes import LeftClick, RightClick
from tests.utils import mouse_stub


def test_mouse_click_performs_left_click() -> None:
    instruction = MouseClick(LeftClick())

    instruction.perform()

    assert mouse_stub.click_calls == 1
    assert instruction.id == 1


def test_mouse_click_performs_right_click() -> None:
    instruction = MouseClick(RightClick())

    instruction.perform()

    assert mouse_stub.right_click_calls == 1


def test_mouse_click_rejects_invalid_click_type() -> None:
    with pytest.raises(TypeError):
        MouseClick(object())
