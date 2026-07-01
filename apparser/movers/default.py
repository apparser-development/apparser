import pyautogui

from apparser.geometry import Point
from apparser.movers.base import BaseMover


class DefaultMover(BaseMover):
    """Move the cursor directly by using the mouse backend."""

    def __init__(self,
                 duration: float = 0):
        """Initialize a direct mouse mover.

        :param duration: Cursor movement duration.
        :type duration: float
        :raises TypeError: If any argument has an invalid type.
        :raises ValueError: If ``duration`` is negative.
        """
        if not (isinstance(duration, float) or isinstance(duration, int)):
            raise TypeError("duration must be a number")

        if duration < 0:
            raise ValueError("duration must be >= 0")

        self.__duration = duration

    def move(self, position: Point):
        """Move the cursor to the target position.

        :param position: Target cursor position.
        :type position: Point
        """
        pyautogui.moveTo(position.x, position.y,
                         duration=self.__duration)
