from __future__ import annotations

from types import ModuleType, SimpleNamespace


class ScreenInfoStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("screeninfo")
        self.reset()

    def reset(self) -> None:
        self.monitors = [SimpleNamespace(width=1920, height=1080)]

    def get_monitors(self) -> list[SimpleNamespace]:
        return self.monitors
