from __future__ import annotations

from apparser.cv import handlers


def test_cv_handlers_exports_expected_symbols() -> None:
    assert set(handlers.__all__) == {"CvHandlers", "DefaultHandlers"}
