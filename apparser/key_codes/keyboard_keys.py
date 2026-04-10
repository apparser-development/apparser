from apparser.key_codes.base import BaseKeyCode


class Enter(BaseKeyCode):
    def __str__(self) -> str:
        return "enter"


class Control(BaseKeyCode):
    def __str__(self) -> str:
        return "ctrl"


class Alt(BaseKeyCode):
    def __str__(self) -> str:
        return "alt"


class Delete(BaseKeyCode):
    def __str__(self) -> str:
        return "del"
