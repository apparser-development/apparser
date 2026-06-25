from functools import singledispatchmethod

import numpy
from appwindows import Window

from apparser.core.ui.base import BaseUi
from apparser.geometry import Point, RelativelyPoint, Size


class CoordinatesUi(BaseUi):
    """Represent a UI region defined by two points inside another UI context."""

    def __init__(
        self,
        from_ui: BaseUi,
        point_one: Point | RelativelyPoint,
        point_two: Point | RelativelyPoint
    ):
        """Initialize a nested coordinate-based UI context.

        :param from_ui: Source UI used as a parent context.
        :type from_ui: BaseUi
        :param point_one: First point of the nested region.
        :type point_one: Point | RelativelyPoint
        :param point_two: Second point of the nested region.
        :type point_two: Point | RelativelyPoint
        :raises TypeError: If any argument has an invalid type.
        """
        if not isinstance(from_ui, BaseUi):
            raise TypeError('from_ui must be BaseUi')

        if not isinstance(point_one, (Point, RelativelyPoint)):
            raise TypeError('point_one must be Point or RelativelyPoint')

        elif not isinstance(point_two, (Point, RelativelyPoint)):
            raise TypeError('point_two must be Point or RelativelyPoint')

        self.__from_ui = from_ui
        self.__point_one = point_one
        self.__point_two = point_two

    def __point_to_main_ui_local(self, point: Point | RelativelyPoint) -> Point:
        if isinstance(point, RelativelyPoint):
            return self.__from_ui.point_to_local(self.__from_ui.point_to_global(point))
        return point

    def __get_local_bounds(self) -> tuple[Point, Point]:
        point1 = self.__point_to_main_ui_local(self.__point_one)
        point2 = self.__point_to_main_ui_local(self.__point_two)
        left_top_point = Point(
            min(point1.x, point2.x),
            min(point1.y, point2.y),
        )
        right_bottom_point = Point(
            max(point1.x, point2.x),
            max(point1.y, point2.y),
        )
        return left_top_point, right_bottom_point

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
    def _(self, coordinates: Point) -> Point:
        left_top_point, _ = self.__get_local_bounds()
        return self.__from_ui.point_to_global(coordinates + left_top_point)

    @point_to_global.register(RelativelyPoint)
    def _(self, coordinates: RelativelyPoint) -> Point:
        left_top_point, right_bottom_point = self.__get_local_bounds()
        width = abs(round(right_bottom_point.x - left_top_point.x))
        height = abs(round(right_bottom_point.y - left_top_point.y))
        x = round(coordinates.x * width)
        y = round(coordinates.y * height)
        local_point = Point(x, y)
        return self.point_to_global(local_point)

    def point_to_local(self, coordinates: Point) -> Point:
        """Convert global coordinates to the local region space.

        :param coordinates: Global point to convert.
        :type coordinates: Point
        :return: Converted local point.
        :rtype: Point
        """
        left_top_point, _ = self.__get_local_bounds()
        return self.__from_ui.point_to_local(coordinates) - left_top_point

    def get_screenshot(self) -> numpy.ndarray:
        """Capture a screenshot cropped to the nested region.

        :return: Screenshot data for the nested region.
        :rtype: numpy.ndarray
        """
        screenshot = self.__from_ui.get_screenshot()
        left_top_point, right_bottom_point = self.__get_local_bounds()
        return screenshot[
            left_top_point.y:right_bottom_point.y,
            left_top_point.x:right_bottom_point.x,
        ]

    @property
    def window(self) -> Window:
        """Return the parent window for the nested region.

        :return: Underlying parent window.
        :rtype: Window
        """
        return self.__from_ui.window
