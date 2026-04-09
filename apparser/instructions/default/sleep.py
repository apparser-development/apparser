import time

from apparser.instructions.base import Instruction


class Sleep(Instruction):
    def __init__(self, sleep_time: float):
        if sleep_time <= 0:
            raise ValueError("sleep_time must be >= 0")

        self.sleep_time = sleep_time

    @property
    def id(self) -> int:
        return 40

    def perform(self, *args, **kwargs):
        time.sleep(self.sleep_time)
