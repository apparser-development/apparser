from __future__ import annotations

import sys
from types import ModuleType
from typing import Any

import numpy
import pytest
from appwindows.geometry import Point, QuadPoints

from apparser.text_readers import RapidOcrReader


class RapidOcrEngineStub:
    instances: list["RapidOcrEngineStub"] = []

    def __init__(self, **settings: Any) -> None:
        self.settings = settings
        self.result: Any = []
        self.calls: list[dict[str, Any]] = []
        self.__class__.instances.append(self)

    def __call__(self, image: numpy.ndarray, **settings: Any) -> Any:
        self.calls.append({"image": image, "settings": settings})
        return self.result


class RapidOcrStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("rapidocr")
        RapidOcrEngineStub.instances = []
        self.RapidOCR = RapidOcrEngineStub


class RapidOcrOutputStub:
    def __init__(self, boxes: list[Any], txts: list[str]) -> None:
        self.boxes = boxes
        self.txts = txts


def assert_quad_points_equal(
    first: QuadPoints,
    second: QuadPoints,
) -> None:
    assert first.left_top == second.left_top
    assert first.right_top == second.right_top
    assert first.right_bottom == second.right_bottom
    assert first.left_bottom == second.left_bottom


def test_rapid_ocr_reader_maps_result_list(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rapidocr_stub = RapidOcrStub()
    monkeypatch.setitem(sys.modules, "rapidocr", rapidocr_stub)
    reader = RapidOcrReader(device="cpu")
    instance = RapidOcrEngineStub.instances[0]
    image = numpy.zeros((2, 2, 3), dtype=numpy.uint8)
    instance.result = [
        (
            [
                [1.1, 2.2],
                [3.3, 4.4],
                [5.5, 6.6],
                [7.7, 8.8],
            ],
            "text",
        ),
    ]

    result = reader.read_image(image, use_det=True)

    expected_points = QuadPoints(
        Point(1, 2),
        Point(3, 4),
        Point(5, 6),
        Point(7, 8),
    )
    assert instance.settings == {"device": "cpu"}
    assert instance.calls[0]["image"] is image
    assert instance.calls[0]["settings"] == {"use_det": True}
    assert result[0].text == "text"
    assert_quad_points_equal(result[0].coordinates, expected_points)


def test_rapid_ocr_reader_maps_output_object(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rapidocr_stub = RapidOcrStub()
    monkeypatch.setitem(sys.modules, "rapidocr", rapidocr_stub)
    reader = RapidOcrReader()
    instance = RapidOcrEngineStub.instances[0]
    instance.result = RapidOcrOutputStub(
        boxes=[
            [1, 2, 3, 4],
        ],
        txts=["text"],
    )

    result = reader.read_image(numpy.zeros((2, 2, 3), dtype=numpy.uint8))

    expected_points = QuadPoints(
        Point(1, 2),
        Point(3, 2),
        Point(3, 4),
        Point(1, 4),
    )
    assert result[0].text == "text"
    assert_quad_points_equal(result[0].coordinates, expected_points)
