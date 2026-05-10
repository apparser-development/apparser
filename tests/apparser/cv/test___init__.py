from __future__ import annotations

from apparser import cv


def test_cv_exports_expected_symbols() -> None:
    assert hasattr(cv, "DefaultHandlers")
    assert hasattr(cv, "DefaultCvProcess")
    assert hasattr(cv, "YoloReader")
    assert hasattr(cv, "CvBox")
