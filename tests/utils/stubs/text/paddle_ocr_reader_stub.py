from __future__ import annotations

from typing import Any

import numpy


class PaddleOcrReaderStub:
    instances: list["PaddleOcrReaderStub"] = []

    def __init__(self, lang: str = "en", **settings: Any) -> None:
        self.lang = lang
        self.settings = settings
        self.predict_result: list[Any] = []
        self.ocr_result: list[Any] = []
        self.predict_calls: list[dict[str, Any]] = []
        self.ocr_calls: list[dict[str, Any]] = []
        self.__class__.instances.append(self)

    def predict(self, image: numpy.ndarray, **settings: Any) -> list[Any]:
        self.predict_calls.append({"image": image, "settings": settings})
        return self.predict_result

    def ocr(self, image: numpy.ndarray, **settings: Any) -> list[Any]:
        self.ocr_calls.append({"image": image, "settings": settings})
        return self.ocr_result
