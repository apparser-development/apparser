import pyautogui

from apparser.instructions.base import BaseInstruction


class WriteText(BaseInstruction):
    """Type text through the keyboard backend."""

    def __init__(self, text: str, pause_time: float = 0.1):
        """Initialize a text writing instruction.

        :param text: Text to type.
        :type text: str
        :param pause_time: Delay between typed characters.
        :type pause_time: float
        :raises TypeError: If ``text`` or ``pause_time`` has an invalid type.
        :raises ValueError: If ``text`` is empty.
        """
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
        return 4

    def perform(self, *args, **kwargs):
        pyautogui.write(self.__text, interval=self.__pause_time)
