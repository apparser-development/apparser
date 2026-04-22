import mouse

from apparser.instructions.base import BaseInstruction
from apparser.key_codes.mouse_keys import RightClick, LeftClick


class MouseClick(BaseInstruction):
    def __init__(self, click_type: RightClick | LeftClick = LeftClick()):
        if isinstance(click_type, RightClick):
            self.__press_function = mouse.right_click
        elif isinstance(click_type, LeftClick):
            self.__press_function = mouse.click
        else:
            raise TypeError('click_type must be RightClick or LeftClick')

        self.__click_type = click_type

    @property
    def id(self) -> int:
        return 21

    def perform(self, *args, **kwargs):
        self.__press_function()