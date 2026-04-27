from apparser.key_codes.base import BaseKeyCode


class Enter(BaseKeyCode):
    """Represent the Enter keyboard key."""

    def __str__(self) -> str:
        """Return the string representation of the Enter key.

        :return: Enter key code.
        :rtype: str
        """
        return "enter"


class Control(BaseKeyCode):
    """Represent the Control keyboard key."""

    def __str__(self) -> str:
        """Return the string representation of the Control key.

        :return: Control key code.
        :rtype: str
        """
        return "ctrl"


class Alt(BaseKeyCode):
    """Represent the Alt keyboard key."""

    def __str__(self) -> str:
        """Return the string representation of the Alt key.

        :return: Alt key code.
        :rtype: str
        """
        return "alt"


class Delete(BaseKeyCode):
    """Represent the Delete keyboard key."""

    def __str__(self) -> str:
        """Return the string representation of the Delete key.

        :return: Delete key code.
        :rtype: str
        """
        return "del"
