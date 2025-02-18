from instructions.default.base import Instruction
from base import Point
from key_codes.mouse_keys import RightClick, LeftClick


class MouseClickTo(Instruction):
    def __init__(self, coordinates: Point, click_type: RightClick | LeftClick):
        self.__coordinates = coordinates
        self.__click_type = click_type

    def perform(self, ui):
        pass
