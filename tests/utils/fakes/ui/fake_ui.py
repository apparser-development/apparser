from __future__ import annotations

import numpy
from appwindows.geometry import Point, Size

from tests.utils.external_stubs import install_external_stubs
from tests.utils.fakes.ui.fake_window import FakeWindow


install_external_stubs()

from apparser.core.ui.base import BaseUi
from apparser.geometry import RelativelyPoint


class FakeUi(BaseUi):
    def __init__(
        self,
        offset: Point | None = None,
        screenshot: numpy.ndarray | None = None,
        window: FakeWindow | None = None,
        relative_size: Size | None = None,
    ) -> None:
        self.offset = offset or Point(0, 0)
        self._screenshot = (
            screenshot
            if screenshot is not None
            else numpy.zeros((20, 20, 3), dtype=numpy.uint8)
        )
        self._window = window or FakeWindow()
        self.relative_size = relative_size or Size(100, 100)

    def point_to_global(self, coordinates: Point | RelativelyPoint) -> Point:
        if isinstance(coordinates, RelativelyPoint):
            x = round(coordinates.x * self.relative_size.width)
            y = round(coordinates.y * self.relative_size.height)
            return Point(self.offset.x + x, self.offset.y + y)
        return Point(self.offset.x + coordinates.x, self.offset.y + coordinates.y)

    def point_to_local(self, coordinates: Point) -> Point:
        return Point(coordinates.x - self.offset.x, coordinates.y - self.offset.y)

    def get_screenshot(self) -> numpy.ndarray:
        return self._screenshot

    @property
    def window(self) -> FakeWindow:
        return self._window
