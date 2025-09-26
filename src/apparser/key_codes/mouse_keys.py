from apparser.key_codes.base import KeyCode


class RightClick(KeyCode):
    def __str__(self) -> str:
        return "RIGHT"


class LeftClick(KeyCode):
    def __str__(self) -> str:
        return "LEFT"
