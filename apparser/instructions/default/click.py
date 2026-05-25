import pyautogui

from apparser.key_codes import RightClick, LeftClick, BaseKeyCode
from apparser.instructions.base import BaseInstruction


class MouseClick(BaseInstruction):
    """Click the selected mouse button."""

    def __init__(self, click_type: BaseKeyCode = LeftClick()):
        """Initialize a mouse click instruction.

        :param click_type: Mouse button to click.
        :type click_type: BaseKeyCode
        :raises TypeError: If ``click_type`` is neither :class:`BaseKeyCode`.
        """
        if not isinstance(click_type, BaseKeyCode):
            raise TypeError('click_type must be BaseKeyCode')

        self.__click_type = click_type

    @property
    def id(self) -> int:
        return 1

    def perform(self, *args, **kwargs):
        pyautogui.click(button=str(self.__click_type))


class MouseDown(BaseInstruction):
    """Press the selected mouse button down."""

    def __init__(self, click_type: BaseKeyCode = LeftClick()):
        """Initialize a mouse down instruction.

        :param click_type: Mouse button to press down.
        :type click_type: BaseKeyCode
        :raises TypeError: If ``click_type`` is neither :class:`BaseKeyCode`.
        """
        if not isinstance(click_type, BaseKeyCode):
            raise TypeError('click_type must be BaseKeyCode')

        self.__click_type = click_type

    @property
    def id(self) -> int:
        return 13

    def perform(self, *args, **kwargs):
        pyautogui.mouseDown(button=str(self.__click_type))


class MouseUp(BaseInstruction):
    """Release the selected mouse button."""

    def __init__(self, click_type: BaseKeyCode = LeftClick()):
        """Initialize a mouse up instruction.

        :param click_type: Mouse button to release.
        :type click_type: BaseKeyCode
        :raises TypeError: If ``click_type`` is neither :class:`BaseKeyCode`.
        """
        if not isinstance(click_type, BaseKeyCode):
            raise TypeError('click_type must be BaseKeyCode')

        self.__click_type = click_type

    @property
    def id(self) -> int:
        return 12

    def perform(self, *args, **kwargs):
        pyautogui.mouseUp(button=str(self.__click_type))
