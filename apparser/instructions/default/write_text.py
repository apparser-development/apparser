import keyboard

from apparser.instructions.default.base import Instruction


class WriteText(Instruction):
    def __init__(self, text: str, pause_time: float = 0.1):
        if not isinstance(text, str):
            raise TypeError('text must be a string')

        if not (isinstance(pause_time, int) or isinstance(pause_time, float)):
            raise TypeError('pause_time must be a number')

        if len(text) < 1:
            raise ValueError('text cannot be empty')

        self.__text = text
        self.__pause_time = pause_time

    @property
    def id(self) -> int:
        return 32

    def perform(self, *args, **kwargs):
        keyboard.write(self.__text, self.__pause_time)
