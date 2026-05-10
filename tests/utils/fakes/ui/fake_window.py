from __future__ import annotations

import numpy
from appwindows.geometry import Point, Size

from tests.utils.fakes.ui.fake_window_points import FakeWindowPoints


class FakeWindow:
    def __init__(
        self,
        left_top: Point | None = None,
        size: Size | None = None,
        screenshot: numpy.ndarray | None = None,
    ) -> None:
        self.left_top = left_top or Point(0, 0)
        self.size = size or Size(100, 100)
        self.screenshot = (
            screenshot
            if screenshot is not None
            else numpy.zeros((10, 10, 3), dtype=numpy.uint8)
        )
        self.move_calls: list[Point] = []
        self.resize_calls: list[Size] = []
        self.to_background_calls = 0
        self.to_foreground_calls = 0
        self.close_calls = 0

    def get_points(self) -> FakeWindowPoints:
        return FakeWindowPoints(left_top=self.left_top)

    def get_size(self) -> Size:
        return self.size

    def get_screenshot(self) -> numpy.ndarray:
        return self.screenshot

    def move(self, position: Point) -> None:
        self.move_calls.append(position)

    def resize(self, size: Size) -> None:
        self.resize_calls.append(size)

    def to_background(self) -> None:
        self.to_background_calls += 1

    def to_foreground(self) -> None:
        self.to_foreground_calls += 1

    def close(self) -> None:
        self.close_calls += 1
