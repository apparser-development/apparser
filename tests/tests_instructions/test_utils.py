"""Tests for instruction utility helpers."""

import pytest

from apparser.instructions.ai.click_on_text import ClickOnText
from apparser.instructions.default.press import PressKey
from apparser.instructions.utils.get_by_id import get_instruction_by_id
from apparser.instructions.utils.get_by_name import get_instruction_by_name


@pytest.mark.parametrize(
    ("instruction_id", "expected"),
    [
        (30, PressKey),
        (102, None),
        (999, None),
    ],
)
def test_get_instruction_by_id(instruction_id, expected):
    assert get_instruction_by_id(instruction_id) is expected


@pytest.mark.parametrize(
    ("instruction_name", "expected"),
    [
        ("PressKey", None),
        ("ClickOnText", None),
        ("UnknownInstruction", None),
    ],
)
def test_get_instruction_by_name(instruction_name, expected):
    assert get_instruction_by_name(instruction_name) is expected


def test_get_instruction_by_id_validation():
    with pytest.raises(TypeError, match="id must be an integer"):
        get_instruction_by_id("1")

    with pytest.raises(ValueError, match="id must be >= 0"):
        get_instruction_by_id(-1)


def test_get_instruction_by_name_validation():
    with pytest.raises(TypeError, match="id must be an str"):
        get_instruction_by_name(1)

    with pytest.raises(ValueError, match="name is empty"):
        get_instruction_by_name("")
