import pyautogui

from apparser.key_codes import BaseKeyCode

from apparser.instructions.base import BaseInstruction


class PressKey(BaseInstruction):
    """Send a single keyboard key press."""

    def __init__(self, key_code: BaseKeyCode | str):
        """Initialize a single-key press instruction.

        :param key_code: Key code to send.
        :type key_code: BaseKeyCode | str
        :raises TypeError: If ``key_code`` is neither :class:`BaseKeyCode` nor :class:`str`.
        """
        if not (isinstance(key_code, BaseKeyCode) or isinstance(key_code, str)):
            raise TypeError('key_code must be BaseKeyCode or str')

        self.__key_code = key_code

    @property
    def id(self) -> int:
        return 2

    def perform(self, *args, **kwargs):
        pyautogui.press(str(self.__key_code))


class PressKeysCombination(BaseInstruction):
    """Send a keyboard shortcut as a pressed combination."""

    def __init__(self, keys: list[BaseKeyCode | str]):
        """Initialize a key combination instruction.

        :param keys: Keys to press together.
        :type keys: list[BaseKeyCode | str]
        """
        self.__keys = keys

    @property
    def id(self) -> int:
        return 3

    def perform(self, *args, **kwargs):
        for key in self.__keys:
            if not (isinstance(key, BaseKeyCode) or isinstance(key, str)):
                raise TypeError('key_code must be BaseKeyCode or str')
            pyautogui.keyDown(str(key))

        for key in self.__keys:
            pyautogui.keyUp(str(key))


class PressKeyDown(BaseInstruction):
    """Send a single keyboard key press down."""

    def __init__(self, key_code: BaseKeyCode | str):
        """Initialize a single-key press down instruction.

        :param key_code: Key code to press down.
        :type key_code: BaseKeyCode | str
        :raises TypeError: If ``key_code`` is neither :class:`BaseKeyCode` nor :class:`str`.
        """
        if not (isinstance(key_code, BaseKeyCode) or isinstance(key_code, str)):
            raise TypeError('key_code must be BaseKeyCode or str')

        self.__key_code = key_code

    @property
    def id(self) -> int:
        return 10

    def perform(self, *args, **kwargs):
        pyautogui.keyDown(str(self.__key_code))


class PressKeyUp(BaseInstruction):
    """Release a single keyboard key."""

    def __init__(self, key_code: BaseKeyCode | str):
        """Initialize a single-key release instruction.

        :param key_code: Key code to release.
        :type key_code: BaseKeyCode | str
        :raises TypeError: If ``key_code`` is neither :class:`BaseKeyCode` nor :class:`str`.
        """
        if not (isinstance(key_code, BaseKeyCode) or isinstance(key_code, str)):
            raise TypeError('key_code must be BaseKeyCode or str')

        self.__key_code = key_code

    @property
    def id(self) -> int:
        return 11

    def perform(self, *args, **kwargs):
        pyautogui.keyUp(str(self.__key_code))
