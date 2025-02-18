from base import Ui
from instructions.default.base import Instruction
from key_codes.base import KeyCode


class PressKey(Instruction):
    def __init__(self, key_code: KeyCode):
        self.__key_code = key_code

    def perform(self, ui: Ui):
        pass


class PressKeysCombination(Instruction):
    def __init__(self, keys: list[PressKey]):
        self.__keys = keys

    def perform(self, ui: Ui):
        for i in self.__keys:
            i.perform(ui)
