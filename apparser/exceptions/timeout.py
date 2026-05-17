class TimeoutException(Exception):
    def __init__(self, wait_time: float | int | None = None):
        if wait_time is None:
            super().__init__(f"Timeout error")

        if not isinstance(wait_time, float) or not isinstance(wait_time, int):
            raise TypeError("min_similarity must be a number")

        if wait_time <= 0:
            raise ValueError("min_similarity must be between 0 and 1")

        super().__init__(f"Timeout error, wait > {wait_time} seconds")
