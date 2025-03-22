from apparser.key_codes.base import KeyCode


class Enter(KeyCode):
    @property
    def key(self) -> str:
        return "enter"


class Control(KeyCode):
    @property
    def key(self) -> str:
        return "ctrl"


class Alt(KeyCode):
    @property
    def key(self) -> str:
        return "alt"


class Delete(KeyCode):
    @property
    def key(self) -> str:
        return "del"
