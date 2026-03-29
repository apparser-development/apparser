class WindowActionWithDesktopException(Exception):
    def __init__(self):
        super().__init__(f"You cannot treat the DesktopUi class as a window.")