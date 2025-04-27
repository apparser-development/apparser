from pyautogui import scroll

from apparser.base import Ui
from apparser.instructions.default.base import Instruction


class ScrollOn(Instruction):
    def __init__(self, deviation: int):
        if isinstance(deviation, int):
            raise ValueError('deviation must be an integer')

        self.__deviation = deviation

    def perform(self, *args, **kwargs):
        scroll(self.__deviation)
