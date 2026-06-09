from __future__ import annotations

import numpy
from appwindows.geometry import Point, QuadPoints

from apparser.text_readers.detectors import EasyOcrDetector
from tests.utils import easyocr_stub


def test_easy_ocr_detector_uses_default_language() -> None:
    EasyOcrDetector()

    instance = easyocr_stub.Reader.instances[0]
    assert instance.lang_list == ["en"]
    assert instance.settings == {
        "detector": True,
        "recognizer": False,
    }


def test_easy_ocr_detector_maps_detected_boxes() -> None:
    detector = EasyOcrDetector(["ru"], gpu=False)
    instance = easyocr_stub.Reader.instances[0]
    image = numpy.zeros((2, 2, 3), dtype=numpy.uint8)
    instance.detected = (
        [
            [
                [1.1, 5.8, 2.2, 4.9],
            ],
        ],
        [
            [
                [
                    [6.1, 7.2],
                    [8.3, 9.4],
                    [10.5, 11.6],
                    [12.7, 13.8],
                ],
            ],
        ],
    )

    result = detector.read_image(image, slope_ths=0.1)

    first_points = QuadPoints(
        Point(1, 2),
        Point(5, 2),
        Point(5, 4),
        Point(1, 4),
    )
    second_points = QuadPoints(
        Point(6, 7),
        Point(8, 9),
        Point(10, 11),
        Point(12, 13),
    )
    assert instance.settings == {
        "detector": True,
        "recognizer": False,
        "gpu": False,
    }
    assert instance.detect_calls[0]["image"] is image
    assert instance.detect_calls[0]["settings"] == {"slope_ths": 0.1}
    assert result[0].left_top == first_points.left_top
    assert result[0].right_top == first_points.right_top
    assert result[0].right_bottom == first_points.right_bottom
    assert result[0].left_bottom == first_points.left_bottom
    assert result[1].left_top == second_points.left_top
    assert result[1].right_top == second_points.right_top
    assert result[1].right_bottom == second_points.right_bottom
    assert result[1].left_bottom == second_points.left_bottom
