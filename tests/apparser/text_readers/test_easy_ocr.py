from __future__ import annotations

import numpy
from appwindows.geometry import Point

from apparser.text_readers.easy_ocr import EasyOcrReader
from tests.utils import easyocr_stub


def test_easy_ocr_reader_uses_default_language() -> None:
    EasyOcrReader()

    instance = easyocr_stub.Reader.instances[0]
    assert instance.lang_list == ["en"]


def test_easy_ocr_reader_maps_prediction_result() -> None:
    reader = EasyOcrReader(["ru"], gpu=False)
    instance = easyocr_stub.Reader.instances[0]
    instance.predicted = [
        (
            [(1.1, 2.8), (3.9, 4.2), (5.0, 6.0), (7.0, 8.0)],
            "text",
            0.99,
        )
    ]

    result = reader.read_image(numpy.zeros((2, 2, 3), dtype=numpy.uint8), detail=1)

    assert instance.settings == {"gpu": False}
    assert instance.read_calls[0]["settings"] == {"detail": 1}
    assert result[0].text == "text"
    assert result[0].coordinates == [
        Point(1, 2),
        Point(3, 4),
        Point(5, 6),
        Point(7, 8),
    ]
