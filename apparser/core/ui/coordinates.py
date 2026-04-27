from functools import singledispatchmethod

import numpy
from appwindows import Window
from appwindows.geometry import Size

from apparser.core.ui.base import BaseUi
from apparser.geometry import Point, RelativelyPoint


class CoordinatesUi(BaseUi):
    """Represent a UI region inside another UI context."""

    def __init__(self,
                 from_ui: BaseUi,
                 left_top_point: Point | RelativelyPoint,
                 size: Size):
        """Initialize a nested coordinate-based UI context.

        :param from_ui: Source UI used as a parent context.
        :type from_ui: BaseUi
        :param left_top_point: Top-left point of the nested region.
        :type left_top_point: Point | RelativelyPoint
        :param size: Size of the nested region.
        :type size: Size
        :raises TypeError: If any argument has an invalid type.
        """
        if not isinstance(from_ui, BaseUi):
            raise TypeError('from_ui must be Ui')

        if not (isinstance(left_top_point, Point) or isinstance(left_top_point, RelativelyPoint)):
            raise TypeError('left_top_point must be Point or RelativelyPoint')

        if not isinstance(size, Size):
            raise TypeError('size must be Size')

        self.__from_ui = from_ui
        self.__left_top_point = left_top_point
        self.__size = size

    def __get_left_top_local_point(self) -> Point:
        if isinstance(self.__left_top_point, RelativelyPoint):
            return self.__from_ui.point_to_local(self.__from_ui.point_to_global(self.__left_top_point))
        return self.__left_top_point

    @singledispatchmethod
    def point_to_global(self, coordinates: Point | RelativelyPoint) -> Point:
        """Convert region coordinates to the global screen space.

        :param coordinates: Local or relative coordinates to convert.
        :type coordinates: Point | RelativelyPoint
        :return: Converted global point.
        :rtype: Point
        """
        raise NotImplementedError()

    @point_to_global.register(Point)
    def _(self, coordinates: Point):
        left_top_point = self.__get_left_top_local_point()
        return self.__from_ui.point_to_global(coordinates + left_top_point)

    @point_to_global.register(RelativelyPoint)
    def _(self, coordinates: RelativelyPoint):
        x = round(coordinates.x * self.__size.width)
        y = round(coordinates.y * self.__size.height)
        local_point = Point(x, y)
        return self.point_to_global(local_point)

    def point_to_local(self, coordinates: Point) -> Point:
        """Convert global coordinates to the local region space.

        :param coordinates: Global point to convert.
        :type coordinates: Point
        :return: Converted local point.
        :rtype: Point
        """
        left_top_point = self.__get_left_top_local_point()
        return self.__from_ui.point_to_local(coordinates) - left_top_point

    def get_screenshot(self) -> numpy.ndarray:
        """Capture a screenshot cropped to the nested region.

        :return: Screenshot data for the nested region.
        :rtype: numpy.ndarray
        """
        screenshot = self.__from_ui.get_screenshot()
        left_top_point = self.__get_left_top_local_point()
        right_bottom_point = left_top_point + Point(self.__size.width, self.__size.height)

        if isinstance(screenshot, numpy.ndarray):
            return screenshot[left_top_point.y:right_bottom_point.y, left_top_point.x:right_bottom_point.x]
        return screenshot.crop((left_top_point.x, left_top_point.y, right_bottom_point.x, right_bottom_point.y))

    @property
    def window(self) -> Window:
        """Return the parent window for the nested region.

        :return: Underlying parent window.
        :rtype: Window
        """
        return self.__from_ui.window
