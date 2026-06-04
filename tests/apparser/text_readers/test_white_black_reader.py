from __future__ import annotations

import numpy

from apparser.text_readers.white_black_reader import WhiteBlackReader
from tests.utils import FakeTextReader


def test_white_black_reader_converts_image_to_grayscale() -> None:
    reader = FakeTextReader(result=["text"])
    wrapped_reader = WhiteBlackReader(reader)
    image = numpy.zeros((3, 3, 3), dtype=numpy.uint8)

    result = wrapped_reader.read_image(image)

    assert result == ["text"]
    assert reader.images[0].ndim == 2
