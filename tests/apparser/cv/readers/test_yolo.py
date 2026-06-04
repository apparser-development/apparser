from __future__ import annotations

from types import SimpleNamespace

import numpy
import pytest

from apparser.cv.readers.yolo import YoloReader
from tests.utils import FakeUi


def test_yolo_reader_uses_existing_model() -> None:
    model = SimpleNamespace(track=lambda **kwargs: [SimpleNamespace(boxes=[])], model=SimpleNamespace(names={}))

    reader = YoloReader(model)

    assert reader._YoloReader__model is model


def test_yolo_reader_creates_model_from_path() -> None:
    reader = YoloReader("weights.pt")

    assert reader._YoloReader__model.model_path == "weights.pt"


def test_yolo_reader_maps_detected_boxes(monkeypatch: pytest.MonkeyPatch) -> None:
    created_uis: list[CoordinatesUiSpy] = []

    class CoordinatesUiSpy:
        def __init__(self, *args: object, **kwargs: object) -> None:
            self.args = args
            self.kwargs = kwargs
            created_uis.append(self)

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
    monkeypatch.setattr("apparser.cv.readers.yolo.CoordinatesUi", CoordinatesUiSpy)

    result = reader.read(ui)

    assert len(result.boxes) == 2
    assert result.boxes[0].class_name == "dog"
    assert result.boxes[0].track_id == 10
    assert result.boxes[0].width == 5
    assert result.boxes[0].height == 6
    assert result.boxes[0].ui is created_uis[0]
    assert result.boxes[1].class_name == "cat"
    assert result.boxes[1].track_id is None
    assert result.boxes[1].ui is created_uis[1]
