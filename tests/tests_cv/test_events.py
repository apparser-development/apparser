"""Tests for CV events."""

from apparser.cv.events import Detected, Moved, Resized, UnDetected


def test_cv_event_strings():
    assert str(Detected()) == "Detected"
    assert str(Moved()) == "Moved"
    assert str(Resized()) == "Resized"
    assert str(UnDetected()) == "UnDetected"
