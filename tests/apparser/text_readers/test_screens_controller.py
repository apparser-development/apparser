from __future__ import annotations

import numpy

from apparser.text_readers.screens_controller import ScreensController
from tests.utils import FakeTextReader


def test_screens_controller_caches_equal_images() -> None:
    reader = FakeTextReader(result=["text"])
    controller = ScreensController(reader)
    image = numpy.zeros((2, 2, 3), dtype=numpy.uint8)

    first = controller.read_image(image)
    second = controller.read_image(image.copy())

    assert first == ["text"]
    assert second == ["text"]
    assert len(reader.images) == 1
