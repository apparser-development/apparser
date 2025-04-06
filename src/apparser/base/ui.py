from functools import singledispatchmethod

from PIL import ImageGrab, Image

from apparser.base.points.absolute import Point
from apparser.base.points.relatively import RelativelyPoint
from apparser.base.window import Window


class Ui:
    def __init__(self, window: Window):
        self.__window = window

    @singledispatchmethod
    def point_to_global(self, coordinates: Point | RelativelyPoint) -> Point:
        raise NotImplementedError()

    @point_to_global.register(Point)
    def _(self, coordinates: Point):
        return coordinates + self.__window.left_top_point

    @point_to_global.register(RelativelyPoint)
    def _(self, coordinates: RelativelyPoint):
        x = round(coordinates.x * self.__window.size[0])
        y = round(coordinates.y * self.__window.size[1])
        local_point = Point(x, y)
        return self.point_to_global(local_point)

    def point_to_local(self, coordinates: Point) -> Point:
        return coordinates - self.__window.left_top_point

    def get_screenshot(self) -> Image:
        image = ImageGrab.grab((self.__window.left_top_point.x, self.__window.left_top_point.y,
                                self.__window.right_bottom_point.x, self.__window.right_bottom_point.y))
        return image

    @property
    def window(self):
        return self.__window
