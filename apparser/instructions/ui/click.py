from apparser.core import BaseUi
from apparser.geometry import Point, RelativelyPoint
from apparser.key_codes import RightClick, LeftClick

from apparser.movers import DefaultMover, BaseMover

from apparser.instructions.ui.base import UiInstruction
from apparser.instructions.default import MouseClick
from apparser.instructions.ui.mouse_move import MouseMove


class MouseClickTo(UiInstruction):
    """Move the cursor to coordinates and click there."""

    def __init__(self, coordinates: Point | RelativelyPoint,
                 click_type: RightClick | LeftClick = LeftClick(),
                 mover: BaseMover = DefaultMover()):
        """Initialize a targeted mouse click instruction.

        :param coordinates: Target click coordinates.
        :type coordinates: Point | RelativelyPoint
        :param click_type: Mouse button to click.
        :type click_type: RightClick | LeftClick
        :param mover: Mouse movement strategy used before the click.
        :type mover: BaseMover
        :raises ValueError: If ``coordinates`` has an invalid type.
        """
        if (not isinstance(coordinates, Point)
                and not isinstance(coordinates, RelativelyPoint)):
            raise ValueError('coordinates must be Point or RelativelyPoint')

        self.__click = MouseClick(click_type)
        self.__move = MouseMove(coordinates, mover=mover)

    @property
    def id(self) -> int:
        return 1005

    def perform(self, ui: BaseUi, *args, **kwargs):
        self.__move.perform(ui)
        self.__click.perform()
