from __future__ import annotations

from apparser.instructions import debuggers


def test_instruction_debuggers_exports_expected_symbols() -> None:
    assert set(debuggers.__all__) == {"BaseDebugger", "Debugger"}
