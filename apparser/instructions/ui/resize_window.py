from apparser.core import BaseUi
from apparser.geometry import Size
from apparser.instructions.ui.base import UiInstruction


class WindowResize(UiInstruction):
    """Resize the current window."""

    def __init__(self, size: Size):
        """Initialize a window resize instruction.

        :param size: Target window size.
        :type size: Size
        :raises TypeError: If ``size`` has an invalid type.
        """
        if not isinstance(size, Size):
            raise TypeError('size must be of type Size')

        self.__size = size

    @property
    def id(self) -> int:
        return 1003

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.resize(self.__size)
