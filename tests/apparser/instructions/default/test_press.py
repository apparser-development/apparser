from __future__ import annotations

import pytest

from apparser.instructions.default.press import PressKey, PressKeysCombination
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


def test_press_keys_combination_rejects_invalid_key_on_perform() -> None:
    instruction = PressKeysCombination([object()])
    with pytest.raises(TypeError):
        instruction.perform()
