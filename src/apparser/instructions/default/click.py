import mouse

from apparser.base import Point, Ui, RelativelyPoint
from apparser.instructions.default.base import Instruction
from apparser.key_codes.mouse_keys import RightClick, LeftClick


class MouseClick(Instruction):
    def __init__(self, click_type: RightClick | LeftClick = LeftClick()):
        if isinstance(click_type, RightClick):
            self.__press_function = mouse.right_click
        elif isinstance(click_type, LeftClick):
            self.__press_function = mouse.click
        else:
            raise ValueError('click_type must be RightClick or LeftClick')

        self.__click_type = click_type

    def perform(self, *args, **kwargs):
        self.__press_function()


class MouseClickTo(Instruction):
    def __init__(self, coordinates: Point | RelativelyPoint, click_type: RightClick | LeftClick = LeftClick()):
        if not isinstance(coordinates, Point):
            raise ValueError('coordinates must be Point')

        self.__click = MouseClick(click_type)
        self.__coordinates = coordinates

    def perform(self, ui: Ui, *args, **kwargs):
        coordinates = ui.point_to_global(self.__coordinates)
        mouse.move(coordinates.x, coordinates.y)
        self.__click.perform()
