import numpy
from appwindows import Window

from apparser.core.ui.base import Ui
from apparser.geometry import Point, RelativelyPoint
from apparser.exceptions import WindowActionWithDesktopException


class DesktopUi(Ui):
    def point_to_global(self, coordinates: Point | RelativelyPoint) -> Point:
        return Point(coordinates.x, coordinates.y)

    def point_to_local(self, coordinates: Point) -> Point:
        raise NotImplementedError()

    def get_screenshot(self) -> numpy.ndarray:
        raise NotImplementedError()

    @property
    def window(self) -> Window:
        raise WindowActionWithDesktopException()
