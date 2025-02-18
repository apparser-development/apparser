from key_codes.base import KeyCode


class Enter(KeyCode):
    @property
    def key(self) -> str:
        return "Entr"


class Control(KeyCode):
    @property
    def key(self) -> str:
        return "Control"