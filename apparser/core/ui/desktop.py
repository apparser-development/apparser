from functools import singledispatchmethod

import numpy
from appwindows import Window
from PIL import ImageGrab
from screeninfo import get_monitors

from apparser.core.ui.base import Ui
from apparser.geometry import Point, RelativelyPoint
from apparser.exceptions import WindowActionWithDesktopException


class DesktopUi(Ui):
    def __init__(self, display_id: int = 0):
        self.__display_id = display_id

    @singledispatchmethod
    def point_to_global(self, coordinates: Point | RelativelyPoint) -> Point:
        raise NotImplementedError()

    @point_to_global.register(Point)
    def _(self, coordinates: Point):
        return coordinates

    @point_to_global.register(RelativelyPoint)
    def _(self, coordinates: RelativelyPoint):
        monitor = get_monitors()[self.__display_id]
        x = round(coordinates.x * monitor.width)
        y = round(coordinates.y * monitor.height)
        local_point = Point(x, y)
        return self.point_to_global(local_point)

    def point_to_local(self, coordinates: Point) -> Point:
        return Point(coordinates.x, coordinates.y)

    def get_screenshot(self) -> numpy.ndarray:
        screenshot = ImageGrab.grab()
        return numpy.asarray(screenshot)

    @property
    def window(self) -> Window:
        raise WindowActionWithDesktopException()
