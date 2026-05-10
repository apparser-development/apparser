from __future__ import annotations

from apparser.core import ui


def test_core_ui_exports_expected_symbols() -> None:
    assert set(ui.__all__) == {"BaseUi", "DesktopUi", "CoordinatesUi", "WindowUi"}
