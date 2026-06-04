from __future__ import annotations

from types import ModuleType
from typing import Any

import numpy


class SoundDeviceStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("sounddevice")
        self.reset()

    def reset(self) -> None:
        self.check_output_settings_calls: list[dict[str, Any]] = []
        self.play_calls: list[dict[str, Any]] = []

    def check_output_settings(self, **kwargs: Any) -> None:
        self.check_output_settings_calls.append(kwargs)

    def play(self, audio: numpy.ndarray, **kwargs: Any) -> None:
        self.play_calls.append({"audio": audio, **kwargs})
