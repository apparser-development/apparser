import abc


class BaseKeyCode(abc.ABC):
    """Define the common interface for key code objects."""

    @abc.abstractmethod
    def __str__(self) -> str:
        """Return the string representation of the key code.

        :return: Key code string value.
        :rtype: str
        """
        pass
