class TimeoutException(Exception):
    """Represent a timeout during a waiting operation."""

    def __init__(self, wait_time: float | int | None = None):
        """Initialize a timeout exception.

        :param wait_time: Time waited before the timeout occurred.
        :type wait_time: float | int | None
        :raises TypeError: If ``wait_time`` has an invalid type.
        :raises ValueError: If ``wait_time`` is negative.
        """
        if wait_time is None:
            super().__init__("Timeout error")
            return

        if not isinstance(wait_time, (float, int)):
            raise TypeError("wait_time must be a number")

        if wait_time < 0:
            raise ValueError("wait_time must be >= 0")

        super().__init__(f"Timeout error. The wait lasted more than {wait_time} seconds.")
