"""Tests for text-reader classes."""

import easyocr
import numpy
from appwindows.geometry import Point

from apparser.text_readers.easy_ocr import EasyOcrReader
from apparser.text_readers.models.text_data import TextData
from apparser.text_readers.screens_controller import ScreensController
from apparser.text_readers.white_black_reader import WhiteBlackReader
from tests.utils.readers import FakeTextReader


def test_easy_ocr_reader_default_lang_and_read_image():
    reader = EasyOcrReader(gpu=False)
    image = numpy.array([[1, 2], [3, 4]])
    easyocr.last_reader.result = [
        (
            [(1.2, 2.8), (3.9, 4.1), (5.7, 6.3), (7.4, 8.6)],
            "hello",
            0.99,
        )
    ]

    result = reader.read_image(image, detail=1)

    assert easyocr.last_reader.lang_list == ["en"]
    assert easyocr.last_reader.settings == {"gpu": False}
    assert easyocr.last_reader.calls == [(image, {"detail": 1})]
    assert result == [
        TextData(
            "hello",
            [Point(1, 2), Point(3, 4), Point(5, 6), Point(7, 8)],
        )
    ]


def test_screens_controller_caches_images():
    ai_reader = FakeTextReader()
    ai_reader.result = [TextData("cached", [Point(0, 0)])]
    controller = ScreensController(ai_reader)
    image = numpy.array([[1, 2], [3, 4]])

    first = controller.read_image(image)
    second = controller.read_image(image.copy())

    assert first == ai_reader.result
    assert second == ai_reader.result
    assert len(ai_reader.calls) == 1


def test_white_black_reader_converts_image_to_grayscale():
    ai_reader = FakeTextReader()
    ai_reader.result = [TextData("gray", [Point(0, 0)])]
    image = numpy.array([[[255, 0, 0], [0, 255, 0]]], dtype=numpy.uint8)

    result = WhiteBlackReader(ai_reader).read_image(image)

    assert result == ai_reader.result
    assert len(ai_reader.calls) == 1
    assert ai_reader.calls[0].ndim == 2
