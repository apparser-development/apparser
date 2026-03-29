from apparser import WindowUi
from apparser.geometry import Size
from apparser.instructions.default.base import Instruction


class ResizeWindow(Instruction):
    def __init__(self, size: Size):
        if not isinstance(size, Size):
            raise TypeError('size must be of type Size')

        self.__size = size

    def perform(self, ui: WindowUi, *args, **kwargs):
        ui.window.resize(self.__size)
