from __future__ import annotations

from typing import Any

import numpy

from tests.utils.external_stubs import install_external_stubs


install_external_stubs()

from apparser.text_readers.base import BaseTextReader


class FakeTextReader(BaseTextReader):
    def __init__(self, result: list[Any] | None = None) -> None:
        self.result = result or []
        self.images: list[numpy.ndarray] = []

    def read_image(self, image: numpy.ndarray) -> list[Any]:
        self.images.append(image)
        return self.result
