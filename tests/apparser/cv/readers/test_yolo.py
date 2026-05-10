from __future__ import annotations

from types import SimpleNamespace

import numpy

from apparser.core.ui.coordinates import CoordinatesUi
from apparser.cv.readers.yolo import YoloReader
from tests.utils import FakeUi, ultralytics_stub


def test_yolo_reader_uses_existing_model() -> None:
    model = SimpleNamespace(track=lambda **kwargs: [SimpleNamespace(boxes=[])], model=SimpleNamespace(names={}))

    reader = YoloReader(model)

    assert reader._YoloReader__model is model


def test_yolo_reader_creates_model_from_path() -> None:
    reader = YoloReader("weights.pt")

    assert reader._YoloReader__model.model_path == "weights.pt"


def test_yolo_reader_maps_detected_boxes() -> None:
    box_with_id = SimpleNamespace(
        id=numpy.asarray([10]),
        cls=numpy.asarray([1]),
        xyxy=numpy.asarray([[1, 2, 6, 8]]),
    )
    box_without_id = SimpleNamespace(
        id=None,
        cls=numpy.asarray([0]),
        xyxy=numpy.asarray([[3, 4, 9, 12]]),
    )
    model = SimpleNamespace(
        model=SimpleNamespace(names={0: "cat", 1: "dog"}),
        track=lambda **kwargs: [SimpleNamespace(boxes=[box_with_id, box_without_id])],
    )
    ui = FakeUi()
    reader = YoloReader(model, persist=False, conf=0.5)

    result = reader.read(ui)

    assert len(result.boxes) == 2
    assert result.boxes[0].class_name == "dog"
    assert result.boxes[0].track_id == 10
    assert result.boxes[0].width == 5
    assert result.boxes[0].height == 6
    assert isinstance(result.boxes[0].ui, CoordinatesUi)
    assert result.boxes[1].class_name == "cat"
    assert result.boxes[1].track_id is None
