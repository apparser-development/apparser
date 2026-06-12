from __future__ import annotations

from apparser.cv.events import Detected, Moved, Resized, UnDetected
from apparser.cv.models import CvAllData, CvBox
from apparser.cv.utils.changes_checker import ChangesChecker, _is_moved, _is_resized
from tests.utils import FakeUi


def test_is_moved_checks_coordinates_difference() -> None:
    ui = FakeUi()
    first = CvBox("button", 1, 1, 2, 3, 4, ui)
    second = CvBox("button", 1, 2, 2, 3, 4, ui)

    assert _is_moved(second, first) is True


def test_is_resized_requires_both_dimensions_to_change() -> None:
    ui = FakeUi()
    first = CvBox("button", 1, 1, 2, 3, 4, ui)
    changed = CvBox("button", 1, 1, 2, 5, 6, ui)
    only_width = CvBox("button", 1, 1, 2, 5, 4, ui)

    assert _is_resized(changed, first) is True
    assert _is_resized(only_width, first) is True
    assert _is_resized(first, first) is False


def test_changes_checker_reports_detected_moved_resized_and_undetected() -> None:
    ui = FakeUi()
    checker = ChangesChecker()
    old_box = CvBox("button", 1, 1, 2, 3, 4, ui)
    checker.check(CvAllData([old_box]))
    new_box = CvBox("button", 1, 2, 3, 5, 6, ui)
    missing_box = CvBox("icon", 2, 9, 9, 1, 1, ui)
    checker.check(CvAllData([new_box, missing_box]))

    next_result = checker.check(CvAllData([new_box]))

    assert next_result[0].event is UnDetected


def test_changes_checker_reports_new_and_changed_boxes_in_order() -> None:
    ui = FakeUi()
    checker = ChangesChecker()
    first_box = CvBox("button", 1, 1, 2, 3, 4, ui)

    initial = checker.check(CvAllData([first_box]))
    changed_box = CvBox("button", 1, 2, 3, 5, 6, ui)
    next_result = checker.check(CvAllData([changed_box]))

    assert initial[0].event is Detected
    assert next_result[0].event is Moved
    assert next_result[1].event is Resized
