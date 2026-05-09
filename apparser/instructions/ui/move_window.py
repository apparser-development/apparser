from apparser.core import BaseUi
from apparser.geometry import Point
from apparser.instructions.ui.base import UiInstruction


class WindowMove(UiInstruction):
    """Move the current window to a new position."""

    def __init__(self, position: Point):
        """Initialize a window move instruction.

        :param position: Target window position.
        :type position: Point
        :raises TypeError: If ``position`` has an invalid type.
        """
        if not isinstance(position, Point):
            raise TypeError('position must be of type Point')

        self.__position = position

    @property
    def id(self) -> int:
        return 1002

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.move(self.__position)
