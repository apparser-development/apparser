from __future__ import annotations

from apparser.cv import events


def test_cv_events_exports_expected_symbols() -> None:
    assert set(events.__all__) == {"CvEvent", "Moved", "Detected", "Resized", "UnDetected"}
