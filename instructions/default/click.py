import mouse

from base import Point, Ui
from instructions.default.base import Instruction
from key_codes.mouse_keys import RightClick, LeftClick


class MouseClickTo(Instruction):
    def __init__(self, coordinates: Point, click_type: RightClick | LeftClick):
        if not isinstance(coordinates, Point):
            raise ValueError('coordinates must be Point')

        if isinstance(click_type, RightClick):
            self.__press_function = mouse.right_click
        elif isinstance(click_type, LeftClick):
            self.__press_function = mouse.click
        else:
            raise ValueError('click_type must be RightClick or LeftClick')

        self.__click_type = click_type
        self.__coordinates = coordinates

    def __call__(self, ui: Ui):
        coordinates = ui.coordinates_to_global(self.__coordinates)
        mouse.move(coordinates.x, coordinates.y)
        self.__press_function()
