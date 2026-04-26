from apparser.core import BaseUi
from apparser.geometry import Point, RelativelyPoint
from apparser.instructions.ui.base import UiInstruction
from apparser.instructions.default import MouseClick
from apparser.instructions.ui.mouse_move import MouseMove
from apparser.key_codes.mouse_keys import RightClick, LeftClick
from apparser.movers import DefaultMover
from apparser.movers.base import BaseMover


class MouseClickTo(UiInstruction):
    def __init__(self, coordinates: Point | RelativelyPoint,
                 click_type: RightClick | LeftClick = LeftClick(),
                 mover: BaseMover = DefaultMover()):
        if (not isinstance(coordinates, Point)
                and not isinstance(coordinates, RelativelyPoint)):
            raise ValueError('coordinates must be Point or RelativelyPoint')

        self.__click = MouseClick(click_type)
        self.__move = MouseMove(coordinates, mover=mover)

    @property
    def id(self) -> int:
        return 105

    def perform(self, ui: BaseUi, *args, **kwargs):
        self.__move.perform(ui)
        self.__click.perform()
