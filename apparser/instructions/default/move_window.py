from apparser.core import Ui
from apparser.geometry import Point
from apparser.instructions.base import Instruction


class WindowMove(Instruction):
    def __init__(self, position: Point):
        if not isinstance(position, Point):
            raise TypeError('position must be of type Point')

        self.__position = position

    @property
    def id(self) -> int:
        return 12

    def perform(self, ui: Ui, *args, **kwargs):
        ui.window.move(self.__position)
