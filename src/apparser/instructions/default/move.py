import mouse

from apparser.base import Point, Ui, RelativelyPoint
from apparser.instructions.default.base import Instruction


class MoveTo(Instruction):
    def __init__(self, coordinates: Point | RelativelyPoint):
        if not isinstance(coordinates, Point):
            raise ValueError('coordinates must be Point')

        self.__coordinates = coordinates

    def __call__(self, ui: Ui, *args, **kwargs):
        coordinates = ui.point_to_global(self.__coordinates)
        mouse.move(coordinates.x, coordinates.y)


class MoveOn(Instruction):
    def __init__(self, coordinates: Point):
        if not isinstance(coordinates, Point):
            raise ValueError('coordinates must be Point')

        self.__coordinates = coordinates

    def __call__(self, ui: Ui, *args, **kwargs):
        mouse.move(self.__coordinates.x, self.__coordinates.y, absolute=False)
