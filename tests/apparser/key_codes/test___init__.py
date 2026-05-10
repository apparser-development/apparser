from __future__ import annotations

from apparser import key_codes


def test_key_codes_exports_expected_symbols() -> None:
    assert set(key_codes.__all__) == {
        "BaseKeyCode",
        "Enter",
        "Control",
        "RightClick",
        "LeftClick",
        "Alt",
        "Delete",
    }
