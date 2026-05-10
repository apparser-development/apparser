from __future__ import annotations

from apparser import text_readers


def test_text_readers_exports_expected_symbols() -> None:
    assert set(text_readers.__all__) == {
        "EasyOcrReader",
        "PaddleTextReader",
        "ScreensController",
        "BaseTextReader",
        "WhiteBlackReader",
        "TextData",
    }
