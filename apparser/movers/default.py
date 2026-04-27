import mouse

from apparser.geometry import Point
from apparser.movers.base import BaseMover


class DefaultMover(BaseMover):
    """Move the cursor directly by using the mouse backend."""

    def __init__(self,
                 duration: float = 0,
                 absolute: bool = True):
        """Initialize a direct mouse mover.

        :param duration: Cursor movement duration.
        :type duration: float
        :param absolute: Whether coordinates are absolute.
        :type absolute: bool
        :raises TypeError: If any argument has an invalid type.
        :raises ValueError: If ``duration`` is negative.
        """
        if not (isinstance(duration, float) or isinstance(duration, int)):
            raise TypeError("Duration must be a number")

        if not isinstance(absolute, bool):
            raise TypeError("Absolute must be a boolean")

        if duration < 0:
            raise ValueError("Duration must be a >= 0")

        self.__absolute = absolute
        self.__duration = duration

    def move(self, position: Point):
        """Move the cursor to the target position.

        :param position: Target cursor position.
        :type position: Point
        """
        mouse.move(position.x, position.y,
                   absolute=self.__absolute,
                   duration=self.__duration)
