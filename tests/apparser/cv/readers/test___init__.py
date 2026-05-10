from __future__ import annotations

from apparser.cv import readers


def test_cv_readers_exports_expected_symbols() -> None:
    assert set(readers.__all__) == {"CvReader", "YoloReader"}
