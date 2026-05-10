from __future__ import annotations

import pytest

from apparser.key_codes.keyboard_keys import Alt, Control, Delete, Enter


@pytest.mark.parametrize(
    ("key_code", "expected"),
    [
        (Enter(), "enter"),
        (Control(), "ctrl"),
        (Alt(), "alt"),
        (Delete(), "del"),
    ],
)
def test_keyboard_key_string_values(key_code: object, expected: str) -> None:
    assert str(key_code) == expected
