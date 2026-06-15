import time

from apparser.instructions.base import BaseInstruction


class Sleep(BaseInstruction):
    """Pause execution for a fixed amount of time."""

    def __init__(self, sleep_time: float):
        """Initialize a sleep instruction.

        :param sleep_time: Delay duration in seconds.
        :type sleep_time: float
        :raises ValueError: If ``sleep_time`` is not greater than zero.
        :raises TypeError: If ``sleep_time`` is not a number.
        """
        if not isinstance(sleep_time, float) and not isinstance(sleep_time, int):
            raise TypeError("sleep_time must be a number.")

        if sleep_time <= 0:
            raise ValueError("sleep_time must be > 0")

        self.sleep_time = sleep_time

    @property
    def id(self) -> int:
        return 9

    def perform(self, *args, **kwargs):
        time.sleep(self.sleep_time)
