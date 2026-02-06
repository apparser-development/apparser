from functools import singledispatchmethod

from PIL import Image
from appwindows import Window
from appwindows.geometry import Point, Size

from apparser.geometry.relatively_point import RelativelyPoint


class Ui:
    def __init__(self, window: Window):
        if not isinstance(window, Window):
            raise TypeError('window must be Window')

        self.__window = window

    @singledispatchmethod
    def point_to_global(self, coordinates: Point | RelativelyPoint) -> Point:
        raise NotImplementedError()

    @point_to_global.register(Point)
    def _(self, coordinates: Point):
        return coordinates + self.__window.get_points()[0]

    @point_to_global.register(RelativelyPoint)
    def _(self, coordinates: RelativelyPoint):
        size: Size = self.__window.get_size()
        x = round(coordinates.x * size.width)
        y = round(coordinates.y * size.height)
        local_point = Point(x, y)
        return self.point_to_global(local_point)

    def point_to_local(self, coordinates: Point) -> Point:
        return coordinates - self.__window.get_points()[0]

    def get_screenshot(self) -> Image:
        return Image.fromarray(self.__window.get_screenshot())

    @property
    def window(self):
        return self.__window
