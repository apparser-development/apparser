"""Reusable CV doubles for tests."""

from types import SimpleNamespace

import numpy

from apparser.core.ui.base import BaseUi
from apparser.cv.models import CvBox


class CvUi(BaseUi):
    """Minimal UI implementation for CV tests."""

    def __init__(self, screenshot=None):
        self._screenshot = (
            numpy.array([[1, 2], [3, 4]])
            if screenshot is None
            else screenshot
        )
        self._window = SimpleNamespace(name="window")

    def point_to_global(self, coordinates):
        return coordinates

    def point_to_local(self, coordinates):
        return coordinates

    def get_screenshot(self):
        return self._screenshot

    @property
    def window(self):
        return self._window


def make_cv_box(
    class_name: str = "cat",
    class_id: int = 1,
    x: int = 0,
    y: int = 0,
    width: int = 1,
    height: int = 1,
    ui: BaseUi | None = None,
) -> CvBox:
    """Create a CV box with a ui UI stub."""

    return CvBox(
        class_name,
        class_id,
        x,
        y,
        width,
        height,
        CvUi() if ui is None else ui,
    )
