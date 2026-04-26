import keyboard

from apparser.instructions.base import BaseInstruction
from apparser.key_codes.base import BaseKeyCode


class PressKey(BaseInstruction):
    def __init__(self, key_code: BaseKeyCode | str):
        if not (isinstance(key_code, BaseKeyCode) or isinstance(key_code, str)):
            raise TypeError('key_code must be KeyCode or str')

        self.__key_code = key_code

    @property
    def id(self) -> int:
        return 2

    def perform(self, *args, **kwargs):
        keyboard.send(str(self.__key_code))


class PressKeysCombination(BaseInstruction):
    def __init__(self, keys: list[BaseKeyCode | str]):
        self.__keys = keys

    @property
    def id(self) -> int:
        return 3

    def perform(self, *args, **kwargs):
        for key in self.__keys:
            if not (isinstance(key, BaseKeyCode) or isinstance(key, str)):
                raise TypeError('key_code must be KeyCode or str')
            keyboard.press(str(key))

        for key in self.__keys:
            keyboard.release(str(key))
