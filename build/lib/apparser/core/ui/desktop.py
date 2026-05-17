from functools import singledispatchmethod

import numpy
from appwindows import Window
from PIL import ImageGrab
from screeninfo import get_monitors

from apparser.core.ui.base import BaseUi
from apparser.geometry import Point, RelativelyPoint
from apparser.exceptions import WindowActionWithDesktopException


class DesktopUi(BaseUi):
    """Represent the full desktop as a UI context."""

    def __init__(self, display_id: int = 0):
        """Initialize a desktop UI context.

        :param display_id: Monitor index used for relative coordinates.
        :type display_id: int
        """
        self.__display_id = display_id

    @singledispatchmethod
    def point_to_global(self, coordinates: Point | RelativelyPoint) -> Point:
        """Convert desktop coordinates to the global screen space.

        :param coordinates: Local or relative coordinates to convert.
        :type coordinates: Point | RelativelyPoint
        :return: Converted global point.
        :rtype: Point
        """
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
        """Convert global coordinates to the desktop local space.

        :param coordinates: Global point to convert.
        :type coordinates: Point
        :return: Converted local point.
        :rtype: Point
        """
        return Point(coordinates.x, coordinates.y)

    def get_screenshot(self) -> numpy.ndarray:
        """Capture a screenshot of the desktop.

        :return: Desktop screenshot data.
        :rtype: numpy.ndarray
        """
        screenshot = ImageGrab.grab()
        return numpy.asarray(screenshot)

    @property
    def window(self) -> Window:
        """Raise an exception because the desktop has no window.

        :raises WindowActionWithDesktopException: Always raised for desktop UI contexts.
        """
        raise WindowActionWithDesktopException()
