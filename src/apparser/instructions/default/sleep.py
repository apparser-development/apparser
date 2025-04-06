import time

from apparser.instructions.default.base import Instruction


class Sleep(Instruction):
    def __init__(self, sleep_time: int):
        if not isinstance(sleep_time, int):
            raise ValueError("sleep_time must be an integer")

        self.sleep_time = sleep_time

    def perform(self, *args, **kwargs):
        time.sleep(self.sleep_time)
