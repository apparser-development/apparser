from apparser.key_codes.base import KeyCode


class Enter(KeyCode):
    def __str__(self) -> str:
        return "enter"


class Control(KeyCode):
    def __str__(self) -> str:
        return "ctrl"


class Alt(KeyCode):
    def __str__(self) -> str:
        return "alt"


class Delete(KeyCode):
    def __str__(self) -> str:
        return "del"
