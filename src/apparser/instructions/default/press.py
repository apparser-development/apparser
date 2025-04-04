import keyboard

from apparser.base import Ui
from apparser.instructions.default.base import Instruction
from apparser.key_codes.base import KeyCode


class PressKey(Instruction):
    def __init__(self, key_code: KeyCode):
        if not isinstance(key_code, KeyCode):
            raise ValueError('key_code must be KeyCode')

        self.__key_code = key_code

    def perform(self, ui: Ui, *args, **kwargs):
        keyboard.send(self.__key_code.key)


class PressKeysCombination(Instruction):
    def __init__(self, keys: list[KeyCode]):
        self.__keys = keys

    def perform(self, ui: Ui, *args, **kwargs):
        for key in self.__keys:
            keyboard.press(key.key)

        for key in self.__keys:
            keyboard.release(key.key)
