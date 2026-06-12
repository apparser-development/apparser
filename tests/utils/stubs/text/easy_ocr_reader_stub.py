from __future__ import annotations

from typing import Any

import numpy


class EasyOcrReaderStub:
    instances: list["EasyOcrReaderStub"] = []

    def __init__(self, lang_list: list[str], **settings: Any) -> None:
        self.lang_list = lang_list
        self.settings = settings
        self.predicted: list[Any] = []
        self.detected: Any = ([], [])
        self.read_calls: list[dict[str, Any]] = []
        self.detect_calls: list[dict[str, Any]] = []
        self.__class__.instances.append(self)

    def readtext(self, image: numpy.ndarray, **settings: Any) -> list[Any]:
        self.read_calls.append({"image": image, "settings": settings})
        return self.predicted

    def detect(self, image: numpy.ndarray, **settings: Any) -> Any:
        self.detect_calls.append({"image": image, "settings": settings})
        return self.detected
