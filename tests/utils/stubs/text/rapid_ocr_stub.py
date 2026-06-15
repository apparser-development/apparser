from __future__ import annotations

from types import ModuleType
from typing import Any

import numpy


class RapidOcrEngineStub:
    instances: list["RapidOcrEngineStub"] = []

    def __init__(self, **settings: Any) -> None:
        self.settings = settings
        self.result: Any = []
        self.calls: list[dict[str, Any]] = []
        self.__class__.instances.append(self)

    def __call__(self, image: numpy.ndarray, **settings: Any) -> Any:
        self.calls.append({"image": image, "settings": settings})
        return self.result


class RapidOcrStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("rapidocr")
        self.reset()

    def reset(self) -> None:
        RapidOcrEngineStub.instances = []
        self.RapidOCR = RapidOcrEngineStub
