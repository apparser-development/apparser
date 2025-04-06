from apparser.key_codes.base import KeyCode


class RightClick(KeyCode):
    @property
    def key(self) -> str:
        return "RIGHT"


class LeftClick(KeyCode):
    @property
    def key(self) -> str:
        return "LEFT"
