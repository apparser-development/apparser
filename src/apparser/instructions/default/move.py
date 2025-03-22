import mouse

from apparser.base import Point, Ui
from apparser.instructions.default.base import Instruction


class MoveTo(Instruction):
    def __init__(self, coordinates: Point):
        if not isinstance(coordinates, Point):
            raise ValueError('coordinates must be Point')

        self.__coordinates = coordinates

    def __call__(self, ui: Ui):
        coordinates = ui.coordinates_to_global(self.__coordinates)
        mouse.move(coordinates.x, coordinates.y)


class MoveOn(Instruction):
    def __init__(self, coordinates: Point):
        if not isinstance(coordinates, Point):
            raise ValueError('coordinates must be Point')

        self.__coordinates = coordinates

    def __call__(self, ui: Ui):
        mouse.move(self.__coordinates.x, self.__coordinates.y, absolute=False)
