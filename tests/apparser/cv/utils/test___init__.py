from __future__ import annotations

from apparser.cv import utils


def test_cv_utils_exports_expected_symbols() -> None:
    assert utils.__all__ == ["ChangesChecker"]
