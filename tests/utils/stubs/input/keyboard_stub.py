from __future__ import annotations

from types import ModuleType


class KeyboardStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("keyboard")
        self.reset()

