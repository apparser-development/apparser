import mouse

from apparser.instructions.base import BaseInstruction
from apparser.key_codes.mouse_keys import RightClick, LeftClick


class MouseClick(BaseInstruction):
    """Click the selected mouse button."""

    def __init__(self, click_type: RightClick | LeftClick = LeftClick()):
        """Initialize a mouse click instruction.

        :param click_type: Mouse button to click.
        :type click_type: RightClick | LeftClick
        :raises TypeError: If ``click_type`` is neither :class:`RightClick` nor :class:`LeftClick`.
        """
        if isinstance(click_type, RightClick):
            self.__press_function = mouse.right_click
        elif isinstance(click_type, LeftClick):
            self.__press_function = mouse.click
        else:
            raise TypeError('click_type must be RightClick or LeftClick')

        self.__click_type = click_type

    @property
    def id(self) -> int:
        return 1

    def perform(self, *args, **kwargs):
        self.__press_function()
