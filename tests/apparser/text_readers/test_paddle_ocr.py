from __future__ import annotations

from types import SimpleNamespace

import numpy
import pytest
from appwindows.geometry import Point

from apparser.text_readers.paddle_ocr import (
    PaddleTextReader,
    _is_ocr_line,
    _parse_ocr_result,
    _parse_predict_result,
)
from tests.utils import paddleocr_stub


def test_parse_predict_result_extracts_text_data() -> None:
    predicted = [
        {
            "rec_texts": ["hello"],
            "rec_polys": [[[1, 2], [3, 4], [5, 6], [7, 8]]],
        },
        SimpleNamespace(
            res={
                "rec_texts": ["world"],
                "dt_polys": [[[8, 7], [6, 5], [4, 3], [2, 1]]],
            }
        ),
        {"rec_texts": ["skip"]},
    ]

    result = _parse_predict_result(predicted)

    assert result[0].text == "hello"
    assert result[0].coordinates == [Point(1, 2), Point(3, 4), Point(5, 6), Point(7, 8)]
    assert result[1].text == "world"
    assert result[1].coordinates == [Point(8, 7), Point(6, 5), Point(4, 3), Point(2, 1)]


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (([[1, 2]], ("text", 0.9)), True),
        ([[[1, 2]], ("text",)], True),
        (None, False),
        ([1], False),
    ],
)
def test_is_ocr_line_detects_expected_shape(value: object, expected: bool) -> None:
    assert _is_ocr_line(value) is expected


def test_parse_ocr_result_supports_nested_data() -> None:
    predicted = [
        [
            (
                [[1, 2], [3, 4], [5, 6], [7, 8]],
                ("hello", 0.9),
            )
        ]
    ]

    result = _parse_ocr_result(predicted)

    assert result[0].text == "hello"
    assert result[0].coordinates == [Point(1, 2), Point(3, 4), Point(5, 6), Point(7, 8)]


def test_paddle_text_reader_uses_predict_when_available() -> None:
    reader = PaddleTextReader(lang="ru")
    instance = paddleocr_stub.PaddleOCR.instances[0]
    instance.predict_result = [
        {
            "rec_texts": ["hello"],
            "rec_polys": [[[1, 1], [2, 2], [3, 3], [4, 4]]],
        }
    ]

    result = reader.read_image(numpy.zeros((2, 2, 3), dtype=numpy.uint8), use_doc_orientation_classify=False)

    assert instance.lang == "ru"
    assert instance.predict_calls[0]["settings"] == {"use_doc_orientation_classify": False}
    assert result[0].text == "hello"


def test_paddle_text_reader_uses_ocr_when_predict_is_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    class ReaderWithoutPredict:
        instances: list["ReaderWithoutPredict"] = []

        def __init__(self, lang: str = "en", **settings: object) -> None:
            self.lang = lang
            self.settings = settings
            self.ocr_calls: list[dict[str, object]] = []
            self.ocr_result = [
                (
                    [[1, 2], [3, 4], [5, 6], [7, 8]],
                    ("hello", 0.8),
                )
            ]
            self.__class__.instances.append(self)

        def ocr(self, image: numpy.ndarray, **settings: object) -> list[object]:
            self.ocr_calls.append({"image": image, "settings": settings})
            return self.ocr_result

    monkeypatch.setattr(paddleocr_stub, "PaddleOCR", ReaderWithoutPredict)
    reader = PaddleTextReader()
    instance = ReaderWithoutPredict.instances[0]

    result = reader.read_image(numpy.zeros((2, 2, 3), dtype=numpy.uint8), det=True)

    assert instance.ocr_calls[0]["settings"] == {"det": True}
    assert result[0].text == "hello"
