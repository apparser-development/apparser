from __future__ import annotations

from apparser import exceptions


def test_exceptions_exports_expected_symbols() -> None:
    assert set(exceptions.__all__) == {
        "TextNotFoundException",
        "WindowActionWithDesktopException",
        "DebugException",
        "InstructionNotFoundException",
        "InstructionWithNameNotFoundException",
        "InstructionWithIdNotFoundException",
    }
