import keyboard

from apparser.instructions.default.base import Instruction


class WriteText(Instruction):
    def __init__(self, text: str, pause_time: float = 0.1):
        self.__text = text
        self.__pause_time = pause_time

    def perform(self, *args, **kwargs):
        keyboard.write(self.__text, self.__pause_time)
