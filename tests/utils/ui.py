"""Reusable UI doubles for tests."""

from appwindows.geometry import Point

from apparser.core.ui.base import BaseUi
from apparser.geometry import RelativelyPoint


class RecordingWindow:
    """Track window interactions."""

    def __init__(self):
        self.calls = []

    def to_foreground(self):
        self.calls.append(("to_foreground",))

    def to_background(self):
        self.calls.append(("to_background",))

    def move(self, position):
        self.calls.append(("move", position))

    def resize(self, size):
        self.calls.append(("resize", size))


class InteractionUi(BaseUi):
    """Simple UI stub for instruction and algorithm tests."""

    def __init__(self, screenshot=None, relative_point: Point | None = None):
        self._window = RecordingWindow()
        self._screenshot = screenshot
        self._relative_point = Point(9, 8) if relative_point is None else relative_point
        self.global_calls = []
        self.local_calls = []

    def point_to_global(self, coordinates):
        self.global_calls.append(coordinates)
        if isinstance(coordinates, RelativelyPoint):
            return self._relative_point
        return coordinates

    def point_to_local(self, coordinates):
        self.local_calls.append(coordinates)
        return coordinates

    def get_screenshot(self):
        return self._screenshot

    @property
    def window(self):
        return self._window
