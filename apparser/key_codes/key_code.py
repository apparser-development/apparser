from apparser.key_codes.base import KeyCode


class KeyboardKeyCode(KeyCode):
    def __init__(self, key: str):
        self.__key = key
        self.__check_keys()

    def __check_keys(self):
        pass

    def __str__(self) -> str:
        return self.__key
