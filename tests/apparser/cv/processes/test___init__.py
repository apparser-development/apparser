from __future__ import annotations

from apparser.cv import processes


def test_cv_processes_exports_expected_symbols() -> None:
    assert set(processes.__all__) == {"CvProcess", "DefaultCvProcess"}
