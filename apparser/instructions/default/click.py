import mouse

from apparser.key_codes import RightClick, LeftClick

from apparser.instructions.base import BaseInstruction


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

    @property
    def id(self) -> int:
        return 1

    def perform(self, *args, **kwargs):
        self.__press_function()


class MouseDown(BaseInstruction):
    """Selected mouse button to down."""

    def __init__(self, click_type: RightClick | LeftClick = LeftClick()):
        """Initialize a mouse down instruction.

        :param click_type: Mouse button to down.
        :type click_type: RightClick | LeftClick
        :raises TypeError: If ``click_type`` is neither :class:`RightClick` nor :class:`LeftClick`.
        """
        if isinstance(click_type, RightClick):
            self.__click_type = mouse.RIGHT
        elif isinstance(click_type, LeftClick):
            self.__click_type = mouse.LEFT
        else:
            raise TypeError('click_type must be RightClick or LeftClick')

    @property
    def id(self) -> int:
        return 13

    def perform(self, *args, **kwargs):
        mouse.press(self.__click_type)


class MouseUp(BaseInstruction):
    """Selected mouse button to up."""

    def __init__(self, click_type: RightClick | LeftClick = LeftClick()):
        """Initialize a mouse click instruction.

       :param click_type: Mouse button to up.
        :type click_type: RightClick | LeftClick
        :raises TypeError: If ``click_type`` is neither :class:`RightClick` nor :class:`LeftClick`.
        """
        if isinstance(click_type, RightClick):
            self.__click_type = mouse.RIGHT
        elif isinstance(click_type, LeftClick):
            self.__click_type = mouse.LEFT
        else:
            raise TypeError('click_type must be RightClick or LeftClick')

    @property
    def id(self) -> int:
        return 12

    def perform(self, *args, **kwargs):
        mouse.release(self.__click_type)
