from __future__ import annotations

import apparser


def test_apparser_exports_core_symbols() -> None:
    assert hasattr(apparser, "App")
    assert hasattr(apparser, "BaseUi")
