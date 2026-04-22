from apparser.core import BaseUi
from apparser.geometry import Point
from apparser.instructions.ui.base import UiInstruction


class WindowMove(UiInstruction):
    def __init__(self, position: Point):
        if not isinstance(position, Point):
            raise TypeError('position must be of type Point')

        self.__position = position

    @property
    def id(self) -> int:
        return 12

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.move(self.__position)
