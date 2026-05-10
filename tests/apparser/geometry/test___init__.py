from __future__ import annotations

from apparser import geometry


def test_geometry_exports_expected_symbols() -> None:
    assert set(geometry.__all__) == {"Point", "Size", "RelativelyPoint", "distance"}
