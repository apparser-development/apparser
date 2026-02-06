import mouse

from apparser.core import Ui
from apparser.geometry import Point, RelativelyPoint
from apparser.instructions.default.base import Instruction
from apparser.instructions.default.mouse_move import MouseMove
from apparser.key_codes.mouse_keys import RightClick, LeftClick
from apparser.movers import DefaultMover
from apparser.movers.base import Mover


class MouseClick(Instruction):
    def __init__(self, click_type: RightClick | LeftClick = LeftClick()):
        if isinstance(click_type, RightClick):
            self.__press_function = mouse.right_click
        elif isinstance(click_type, LeftClick):
            self.__press_function = mouse.click
        else:
            raise TypeError('click_type must be RightClick or LeftClick')

        self.__click_type = click_type

    def perform(self, *args, **kwargs):
        self.__press_function()


class MouseClickTo(Instruction):
    def __init__(self, coordinates: Point | RelativelyPoint,
                 click_type: RightClick | LeftClick = LeftClick(),
                 mover: Mover = DefaultMover()):
        if (not isinstance(coordinates, Point)
                and not isinstance(coordinates, RelativelyPoint)):
            raise ValueError('coordinates must be Point or RelativelyPoint')

        self.__click = MouseClick(click_type)
        self.__move = MouseMove(coordinates, mover=mover)
        self.__coordinates = coordinates

    def perform(self, ui: Ui, *args, **kwargs):
        self.__move.perform(ui)
        self.__click.perform()
