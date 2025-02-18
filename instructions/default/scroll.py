from base import Ui
from instructions.default.base import Instruction


class ScrollOn(Instruction):
    def __init__(self, deviation: int):
        self.__deviation = deviation

    def perform(self, ui: Ui):
        pass
