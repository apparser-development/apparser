from __future__ import annotations

import pytest

from apparser.instructions.default.click import MouseClick, MouseDown, MouseUp
from apparser.key_codes import LeftClick, RightClick
from tests.utils import pyautogui_stub


def test_mouse_click_performs_left_click() -> None:
    instruction = MouseClick(LeftClick())

    instruction.perform()

    assert pyautogui_stub.click_calls == 1
    assert instruction.id == 1


def test_mouse_click_performs_right_click() -> None:
    instruction = MouseClick(RightClick())

    instruction.perform()

    assert pyautogui_stub.click_calls == 1


def test_mouse_click_rejects_invalid_click_type() -> None:
    with pytest.raises(TypeError):
        MouseClick(object())


def test_mouse_down_presses_left_button() -> None:
    instruction = MouseDown(LeftClick())

    instruction.perform()

    assert pyautogui_stub.mouse_down_calls == ["LEFT"]
    assert instruction.id == 13


def test_mouse_down_rejects_invalid_click_type() -> None:
    with pytest.raises(TypeError):
        MouseDown(object())


def test_mouse_up_releases_right_button() -> None:
    instruction = MouseUp(RightClick())

    instruction.perform()

    assert pyautogui_stub.mouse_up_calls == ["RIGHT"]
    assert instruction.id == 12


def test_mouse_up_rejects_invalid_click_type() -> None:
    with pytest.raises(TypeError):
        MouseUp(object())
