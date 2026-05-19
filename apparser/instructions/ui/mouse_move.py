from apparser.core import BaseUi
from apparser.geometry import Point, RelativelyPoint

from apparser.movers import DefaultMover, BaseMover

from apparser.instructions.ui.base import UiInstruction


class MouseMove(UiInstruction):
    """Move the mouse cursor to the provided coordinates."""

    def __init__(self,
                 coordinates: Point | RelativelyPoint,
                 mover: BaseMover = DefaultMover()):
        """Initialize a mouse movement instruction.

        :param coordinates: Target coordinates for the cursor.
        :type coordinates: Point | RelativelyPoint
        :param mover: Mouse movement strategy.
        :type mover: BaseMover
        :raises TypeError: If ``coordinates`` or ``mover`` has an invalid type.
        """
        if not (isinstance(coordinates, Point) or isinstance(coordinates, RelativelyPoint)):
            raise TypeError('coordinates must be Point or RelativelyPoint')

        if not isinstance(mover, BaseMover):
            raise TypeError('mover must be BaseMover')

        self.__mover = mover
        self.__coordinates = coordinates

    @property
    def id(self) -> int:
        return 1004

    def perform(self, ui: BaseUi, *args, **kwargs):
        coordinates = ui.point_to_global(self.__coordinates)
        self.__mover.move(coordinates)
