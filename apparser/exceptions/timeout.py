class TimeoutException(Exception):
    def __init__(self, wait_time: float | int | None = None):
        if wait_time is None:
            super().__init__("Timeout error")
            return

        if not isinstance(wait_time, (float, int)):
            raise TypeError("wait_time must be a number")

        if wait_time < 0:
            raise ValueError("wait_time must be >= 0")

        super().__init__(f"Timeout error. The wait lasted more than {wait_time} seconds.")
