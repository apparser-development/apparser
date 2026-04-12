"""Tests for CV readers."""

from appwindows.geometry import Point
import numpy
import pytest
import ultralytics

from apparser.core.ui.coordinates import CoordinatesUi
from apparser.cv.readers.yolo import YoloReader
from tests.utils.cv import CvUi


def test_yolo_reader_init_and_read():
    reader = YoloReader(model="fake.pt")
    fake_box = type(
        "FakeBox",
        (),
        {
            "id": type("FakeId", (), {"item": staticmethod(lambda: 42)})(),
            "cls": type("FakeCls", (), {"item": staticmethod(lambda: 0)})(),
            "xyxy": [type("FakeCoords", (), {"tolist": staticmethod(lambda: [1.2, 2.4, 8.8, 12.9])})()],
        },
    )()
    ultralytics.last_model.model.names = {0: "cat"}
    ultralytics.last_model.results = [type("FakeResult", (), {"boxes": [fake_box]})()]
    image = numpy.array([[1, 2], [3, 4]])
    ui = CvUi(image)

    result = reader.read(ui)

    assert ultralytics.last_model.kwargs == {"model": "fake.pt"}
    assert ultralytics.last_model.calls == []
    assert ultralytics.last_model.track_calls == [(image, True, {})]
    assert len(result.boxes) == 1
    assert result.boxes[0].class_name == "cat"
    assert result.boxes[0].track_id == 42
    assert result.boxes[0].x == 1
    assert result.boxes[0].y == 2
    assert result.boxes[0].width == 7
    assert result.boxes[0].height == 10
    assert isinstance(result.boxes[0].ui, CoordinatesUi)
    assert result.boxes[0].ui.point_to_global(Point(0, 0)) == Point(1, 2)


def test_yolo_reader_raises_when_tracking_ids_are_missing():
    reader = YoloReader(model="fake.pt")
    fake_box = type(
        "FakeBox",
        (),
        {
            "id": None,
            "cls": type("FakeCls", (), {"item": staticmethod(lambda: 0)})(),
            "xyxy": [type("FakeCoords", (), {"tolist": staticmethod(lambda: [1.2, 2.4, 8.8, 12.9])})()],
        },
    )()
    ultralytics.last_model.model.names = {0: "cat"}
    ultralytics.last_model.results = [type("FakeResult", (), {"boxes": [fake_box]})()]

    with pytest.raises(ValueError, match="tracking did not return object ids"):
        reader.read(CvUi(numpy.array([[1, 2], [3, 4]])))
