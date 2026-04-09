from apparser.core import Ui
from apparser.geometry import Size
from apparser.instructions.base import Instruction


class WindowResize(Instruction):
    def __init__(self, size: Size):
        if not isinstance(size, Size):
            raise TypeError('size must be of type Size')

        self.__size = size

    @property
    def id(self) -> int:
        return 13

    def perform(self, ui: Ui, *args, **kwargs):
        ui.window.resize(self.__size)
