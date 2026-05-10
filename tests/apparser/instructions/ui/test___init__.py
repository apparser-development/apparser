from __future__ import annotations

from apparser.instructions import ui


def test_instruction_ui_exports_expected_symbols() -> None:
    assert set(ui.__all__) == {
        "MouseMove",
        "MouseClickTo",
        "UiInstruction",
        "WindowMove",
        "WindowResize",
        "WindowToForeground",
        "WindowToBackground",
    }
