"""Tests for CV data models."""

from apparser.cv.events import Detected
from apparser.cv.models import CvAllData, CvChangeData
from tests.utils.cv import CvUi, make_cv_box


def test_cv_models_store_data():
    ui = CvUi()
    box = make_cv_box(class_name="bird", class_id=3, x=7, y=8, width=9, height=10, ui=ui)
    all_data = CvAllData([box])
    change = CvChangeData(Detected, box, box)

    assert box.class_name == "bird"
    assert box.track_id == 3
    assert box.x == 7
    assert box.y == 8
    assert box.width == 9
    assert box.height == 10
    assert box.ui is ui
    assert all_data.boxes == [box]
    assert change.event is Detected
    assert change.box is box
    assert change.old_box is box
