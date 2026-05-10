from __future__ import annotations

import numpy

from tests.utils.external_stubs import install_external_stubs


install_external_stubs()

from apparser.speakers.base import BaseSpeaker


class FakeSpeaker(BaseSpeaker):
    def __init__(self, result: numpy.ndarray | None = None) -> None:
        self.result = (
            result if result is not None else numpy.asarray([], dtype=numpy.float32)
        )
        self.calls: list[str] = []

    def speak(self, text: str) -> numpy.ndarray:
        self.calls.append(text)
        return self.result
