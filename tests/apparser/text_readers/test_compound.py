from __future__ import annotations

from typing import Any

import numpy
import pytest
from appwindows.geometry import Point, QuadPoints

from apparser.text_readers import CompoundReader
from apparser.text_readers.detectors import BaseTextDetector
from apparser.text_readers.scanners import BaseTextScanner


class DetectorStub(BaseTextDetector):
    def __init__(self, result: list[QuadPoints]) -> None:
        self.result = result
        self.images: list[numpy.ndarray] = []

    def read_image(self, image: numpy.ndarray) -> list[QuadPoints]:
        self.images.append(image)
        return self.result


class ScannerStub(BaseTextScanner):
    def __init__(self, result: str) -> None:
        self.result = result
        self.images: list[numpy.ndarray] = []

    def read_image(self, image: numpy.ndarray) -> str:
        self.images.append(image)
        return self.result


def assert_quad_points_equal(
    first: QuadPoints,
    second: QuadPoints,
) -> None:
    assert first.left_top == second.left_top
    assert first.right_top == second.right_top
    assert first.right_bottom == second.right_bottom
    assert first.left_bottom == second.left_bottom


@pytest.mark.parametrize(
    ("detector", "scanner"),
    [
        (object(), ScannerStub("text")),
        (DetectorStub([]), object()),
    ],
)
def test_compound_reader_rejects_invalid_backends(
    detector: Any,
    scanner: Any,
) -> None:
    with pytest.raises(TypeError):
        CompoundReader(detector, scanner)


def test_compound_reader_detects_and_scans_text() -> None:
    coordinates = QuadPoints(
        Point(1, 1),
        Point(3, 1),
        Point(3, 3),
        Point(1, 3),
    )
    detector = DetectorStub([coordinates])
    scanner = ScannerStub("text")
    reader = CompoundReader(detector, scanner)
    image = numpy.zeros((4, 4, 3), dtype=numpy.uint8)

    result = reader.read_image(image)

    assert detector.images[0] is image
    assert scanner.images[0].shape == (2, 2, 3)
    assert result[0].text == "text"
    assert_quad_points_equal(result[0].coordinates, coordinates)
