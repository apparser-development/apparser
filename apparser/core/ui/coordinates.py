from functools import singledispatchmethod

import numpy
from appwindows import Window
from appwindows.geometry import Size

from apparser.core.ui.base import Ui
from apparser.geometry import Point, RelativelyPoint


class CoordinatesUi(Ui):
    def __init__(self,
                 from_ui: Ui,
                 left_top_point: Point | RelativelyPoint,
                 size: Size):
        if not isinstance(from_ui, Ui):
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
        left_top_point = self.__get_left_top_local_point()
        return self.__from_ui.point_to_local(coordinates) - left_top_point

    def get_screenshot(self) -> numpy.ndarray:
        screenshot = self.__from_ui.get_screenshot()
        left_top_point = self.__get_left_top_local_point()
        right_bottom_point = left_top_point + Point(self.__size.width, self.__size.height)

        if isinstance(screenshot, numpy.ndarray):
            return screenshot[left_top_point.y:right_bottom_point.y, left_top_point.x:right_bottom_point.x]
        return screenshot.crop((left_top_point.x, left_top_point.y, right_bottom_point.x, right_bottom_point.y))

    @property
    def window(self) -> Window:
        return self.__from_ui.window
