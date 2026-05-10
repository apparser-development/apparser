from __future__ import annotations

from apparser.cv import models


def test_cv_models_exports_expected_symbols() -> None:
    assert set(models.__all__) == {"CvAllData", "CvChangeData", "CvHandler", "CvBox"}
