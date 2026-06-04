from __future__ import annotations

from appwindows.geometry import Point

from apparser.cv.events import Detected
from apparser.cv.models.data import CvAllData, CvBox, CvChangeData
from tests.utils import FakeUi


def test_cv_box_and_related_dataclasses_store_values() -> None:
    ui = FakeUi()
    box = CvBox("button", 1, 2, 3, 4, 5, ui)
    change = CvChangeData(Detected, box, box)
    all_data = CvAllData([box])

    assert box.class_name == "button"
    assert box.track_id == 1
    assert change.event is Detected
    assert all_data.boxes == [box]
