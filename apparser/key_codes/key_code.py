from apparser.key_codes.base import BaseKeyCode


class KeyboardKeyCode(BaseKeyCode):
    """Store a custom keyboard key code."""

    def __init__(self, key: str):
        """Initialize a custom keyboard key code.

        :param key: String representation of the key code.
        :type key: str
        """
        self.__key = key
        self.__check_keys()

    def __check_keys(self):
        pass

    def __str__(self) -> str:
        """Return the stored key code string.

        :return: Stored key code.
        :rtype: str
        """
        return self.__key
