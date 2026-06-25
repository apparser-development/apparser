from __future__ import annotations

import pytest

from apparser.instructions.default.press import (
    PressKey,
    PressKeyDown,
    PressKeysCombination,
    PressKeyUp,
)
from apparser.key_codes import Control
from tests.utils import pyautogui_stub


def test_press_key_sends_key() -> None:
    instruction = PressKey(Control())
    instruction.perform()
    assert pyautogui_stub.send_calls == ["ctrl"]
    assert instruction.id == 2


def test_press_key_rejects_invalid_key() -> None:
    with pytest.raises(TypeError):
        PressKey(object())


def test_press_keys_combination_presses_and_releases_keys() -> None:
    instruction = PressKeysCombination([Control(), "a"])
    instruction.perform()
    assert pyautogui_stub.press_calls == ["ctrl", "a"]
    assert pyautogui_stub.release_calls == ["ctrl", "a"]
    assert instruction.id == 3


def test_press_keys_combination_treats_string_as_one_key() -> None:
    instruction = PressKeysCombination("ctrl")
    instruction.perform()
    assert pyautogui_stub.press_calls == ["ctrl"]
    assert pyautogui_stub.release_calls == ["ctrl"]


def test_press_keys_combination_rejects_invalid_keys_type() -> None:
    with pytest.raises(TypeError):
        PressKeysCombination(object())


def test_press_keys_combination_rejects_invalid_key_on_perform() -> None:
    with pytest.raises(TypeError):
        PressKeysCombination([object()])


def test_press_key_down_sends_key_down() -> None:
    instruction = PressKeyDown(Control())
    instruction.perform()
    assert pyautogui_stub.press_calls == ["ctrl"]
    assert instruction.id == 10


def test_press_key_down_rejects_invalid_key() -> None:
    with pytest.raises(TypeError):
        PressKeyDown(object())


def test_press_key_up_releases_key() -> None:
    instruction = PressKeyUp("a")
    instruction.perform()
    assert pyautogui_stub.release_calls == ["a"]
    assert instruction.id == 11


def test_press_key_up_rejects_invalid_key() -> None:
    with pytest.raises(TypeError):
        PressKeyUp(object())
