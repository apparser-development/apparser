from __future__ import annotations

from types import ModuleType
from typing import Any


class PyAutoGuiFake(ModuleType):
    def __init__(self) -> None:
        super().__init__("pyautogui")
        self.reset()

    def reset(self) -> None:
        self.move_calls: list[dict[str, Any]] = []
        self.click_calls = 0
        self._position = (0, 0)
        self.send_calls: list[str] = []
        self.write_calls: list[tuple[str, float]] = []
        self.press_calls: list[str] = []
        self.release_calls: list[str] = []

    def moveTo(
        self,
        x: int,
        y: int,
        duration: float = 0,
    ) -> None:
        self.move_calls.append(
            {
                "x": x,
                "y": y,
                "duration": duration,
            }
        )
        self._position = (x, y)

    def click(self, button: str) -> None:
        self.click_calls += 1

    def position(self) -> tuple[int, int]:
        return self._position


    def write(self, text: str, interval: float) -> None:
        self.write_calls.append((text, interval))

    def press(self, key: str) -> None:
        self.send_calls.append(key)

    def keyDown(self, key: str) -> None:
        self.press_calls.append(key)

    def keyUp(self, key: str) -> None:
        self.release_calls.append(key)

    def release(self, key: str) -> None:
        self.release_calls.append(key)

