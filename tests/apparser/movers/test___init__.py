from __future__ import annotations

from apparser import movers


def test_movers_exports_expected_symbols() -> None:
    assert set(movers.__all__) == {"DefaultMover", "AntiRobotMover"}
