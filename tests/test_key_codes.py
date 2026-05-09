"""Tests for key-code classes."""

import pytest

from apparser.key_codes import (
    Alt,
    Control,
    Delete,
    Enter,
    LeftClick,
    RightClick,
)


@pytest.mark.parametrize(
    ("key_code", "expected"),
    [
        (Enter(), "enter"),
        (Control(), "ctrl"),
        (Alt(), "alt"),
        (Delete(), "del"),
        (RightClick(), "RIGHT"),
        (LeftClick(), "LEFT"),
    ],
)
def test_predefined_key_codes_to_string(key_code, expected):
    assert str(key_code) == expected
