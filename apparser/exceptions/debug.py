class DebugException(Exception):
    def __init__(self, message: str):
        if not isinstance(message, str):
            raise TypeError("message must be a string")

        super().__init__(message)