from __future__ import annotations

from apparser import core


def test_core_exports_expected_symbols() -> None:
    assert set(core.__all__) == {"App", "BaseUi", "DesktopUi", "CoordinatesUi", "WindowUi"}
