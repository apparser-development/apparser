from __future__ import annotations

from types import ModuleType


class KeyboardStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("keyboard")
        self.reset()

    def reset(self) -> None:
        self.send_calls: list[str] = []
        self.write_calls: list[tuple[str, float]] = []
        self.press_calls: list[str] = []
        self.release_calls: list[str] = []

    def send(self, key: str) -> None:
        self.send_calls.append(key)

    def write(self, text: str, pause: float) -> None:
        self.write_calls.append((text, pause))

    def press(self, key: str) -> None:
        self.press_calls.append(key)

    def release(self, key: str) -> None:
        self.release_calls.append(key)
