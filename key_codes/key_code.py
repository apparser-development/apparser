from key_codes.base import KeyCode


class KeyboardKeyCode(KeyCode):
    def __init__(self, key: str):
        self.__key = ""

    @property
    def key(self) -> str:
        return self.__key