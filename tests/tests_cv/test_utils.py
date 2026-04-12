"""Tests for CV utilities."""

import pytest

from apparser.cv.events import Detected, Moved, Resized, UnDetected
from apparser.cv.models import CvAllData, CvChangeData
from apparser.cv.utils.changes_checker import ChangesChecker, _is_moved, _is_resized
from tests.utils.cv import CvUi, make_cv_box


def test_changes_checker_helpers():
    ui = CvUi()
    old_box = make_cv_box(x=1, y=1, width=10, height=10, ui=ui)
    moved_and_resized = make_cv_box(x=2, y=3, width=12, height=13, ui=ui)
    only_x_changed = make_cv_box(x=2, y=1, width=12, height=13, ui=ui)

    assert _is_moved(moved_and_resized, old_box) is True
    assert _is_moved(only_x_changed, old_box) is False
    assert _is_resized(moved_and_resized, old_box) is True
    assert _is_resized(make_cv_box(x=2, y=3, width=12, height=10, ui=ui), old_box) is False


def test_changes_checker_initial_state_raises():
    with pytest.raises(AttributeError):
        ChangesChecker().check(CvAllData([]))


def test_changes_checker_check_with_preloaded_old_data():
    checker = ChangesChecker()
    old_ui = CvUi()
    new_ui = CvUi()
    old_cat = make_cv_box(x=0, y=0, width=10, height=10, ui=old_ui)
    old_dog = make_cv_box(class_name="dog", class_id=2, x=5, y=5, width=20, height=20, ui=old_ui)
    new_cat = make_cv_box(x=1, y=1, width=12, height=12, ui=new_ui)
    new_bird = make_cv_box(class_name="bird", class_id=3, x=7, y=8, width=9, height=10, ui=new_ui)
    checker._ChangesChecker__old_data = CvAllData([old_cat, old_dog])
    data = CvAllData([new_cat, new_bird])

    result = checker.check(data)

    assert result == [
        CvChangeData(UnDetected, old_dog, old_dog),
        CvChangeData(Moved, new_cat, old_cat),
        CvChangeData(Resized, new_cat, old_cat),
        CvChangeData(Detected, new_bird, new_bird),
    ]
