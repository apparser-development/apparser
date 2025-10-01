from apparser import Ui
from apparser.geometry import Point
from apparser.instructions.default.base import Instruction


class MoveWindow(Instruction):
    def __init__(self, position: Point):
        if not isinstance(position, Point):
            raise TypeError('position must be of type Point')

        self.__position = position

    def perform(self, ui: Ui, *args, **kwargs):
        ui.window.move(self.__position)
