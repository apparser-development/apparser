class WindowActionWithDesktopException(Exception):
    """Represent an invalid window action on a desktop UI context."""

    def __init__(self):
        """Initialize a desktop window action exception."""
        super().__init__(f"You cannot treat the DesktopUi class as a window.")
