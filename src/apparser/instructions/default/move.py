import mouse

from apparser.core import Ui
from apparser.geometry import Point, RelativelyPoint
from apparser.instructions.default.base import Instruction


class MoveTo(Instruction):
    def __init__(self, coordinates: Point | RelativelyPoint):
        if not isinstance(coordinates, Point) and not isinstance(coordinates, RelativelyPoint):
            raise TypeError('coordinates must be Point or RelativelyPoint')

        self.__coordinates = coordinates

    def perform(self, ui: Ui, *args, **kwargs):
        coordinates = ui.point_to_global(self.__coordinates)
        mouse.move(coordinates.x, coordinates.y)


class MoveOn(Instruction):
    def __init__(self, coordinates: Point):
        if not isinstance(coordinates, Point) and not isinstance(coordinates, RelativelyPoint):
            raise TypeError('coordinates must be Point or RelativelyPoint')

        self.__coordinates = coordinates

    def perform(self, ui: Ui, *args, **kwargs):
        mouse.move(self.__coordinates.x, self.__coordinates.y, absolute=False)
