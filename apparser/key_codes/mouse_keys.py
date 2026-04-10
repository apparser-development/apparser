from apparser.key_codes.base import BaseKeyCode


class RightClick(BaseKeyCode):
    def __str__(self) -> str:
        return "RIGHT"


class LeftClick(BaseKeyCode):
    def __str__(self) -> str:
        return "LEFT"
