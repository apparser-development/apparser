class DebugException(Exception):
    """Represent an exception enriched with debugging details."""

    def __init__(self, message: str):
        """Initialize a debug exception.

        :param message: Error message with debugging details.
        :type message: str
        :raises TypeError: If ``message`` has an invalid type.
        """
        if not isinstance(message, str):
            raise TypeError("message must be a string")

        super().__init__(message)
