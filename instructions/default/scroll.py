from pyautogui import scroll

from base import Ui
from instructions.default.base import Instruction


class ScrollOn(Instruction):
    def __init__(self, deviation: int):
        if isinstance(deviation, int):
            raise ValueError('deviation must be an integer')

        self.__deviation = deviation

    def __call__(self, ui: Ui):
        scroll(self.__deviation)
