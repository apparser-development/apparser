from __future__ import annotations

from types import ModuleType
from typing import Any


class MouseStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("mouse")
        self.reset()

    def reset(self) -> None:
        self.move_calls: list[dict[str, Any]] = []
        self.click_calls = 0
        self.right_click_calls = 0
        self.position = (0, 0)

    def move(
        self,
        x: int,
        y: int,
        absolute: bool = True,
        duration: float = 0,
    ) -> None:
        self.move_calls.append(
            {
                "x": x,
                "y": y,
                "absolute": absolute,
                "duration": duration,
            }
        )
        self.position = (x, y)

    def click(self) -> None:
        self.click_calls += 1

    def right_click(self) -> None:
        self.right_click_calls += 1

    def get_position(self) -> tuple[int, int]:
        return self.position
