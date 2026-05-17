import abc

from apparser.geometry import Point


class BaseMover(abc.ABC):
    """Define the common interface for cursor movement backends."""

    @abc.abstractmethod
    def move(self, position: Point):
        """Move the cursor to the target position.

        :param position: Target cursor position.
        :type position: Point
        """
        pass
