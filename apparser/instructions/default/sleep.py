import time

from apparser.instructions.base import BaseInstruction


class Sleep(BaseInstruction):
    def __init__(self, sleep_time: float):
        if sleep_time <= 0:
            raise ValueError("sleep_time must be >= 0")

        self.sleep_time = sleep_time

    @property
    def id(self) -> int:
        return 9

    def perform(self, *args, **kwargs):
        time.sleep(self.sleep_time)
