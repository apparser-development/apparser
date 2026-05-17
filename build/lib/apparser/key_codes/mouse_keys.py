from apparser.key_codes.base import BaseKeyCode


class RightClick(BaseKeyCode):
    """Represent the right mouse button."""

    def __str__(self) -> str:
        """Return the string representation of the right mouse button.

        :return: Right mouse button code.
        :rtype: str
        """
        return "RIGHT"


class LeftClick(BaseKeyCode):
    """Represent the left mouse button."""

    def __str__(self) -> str:
        """Return the string representation of the left mouse button.

        :return: Left mouse button code.
        :rtype: str
        """
        return "LEFT"
