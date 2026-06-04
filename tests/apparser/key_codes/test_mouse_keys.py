from __future__ import annotations

import pytest

from apparser.key_codes.mouse_keys import LeftClick, RightClick


@pytest.mark.parametrize(
    ("key_code", "expected"),
    [
        (RightClick(), "RIGHT"),
        (LeftClick(), "LEFT"),
    ],
)
def test_mouse_key_string_values(key_code: object, expected: str) -> None:
    assert str(key_code) == expected
