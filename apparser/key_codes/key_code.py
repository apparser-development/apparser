from apparser.key_codes.base import BaseKeyCode


class KeyboardKeyCode(BaseKeyCode):
    def __init__(self, key: str):
        self.__key = key
        self.__check_keys()

    def __check_keys(self):
        pass

    def __str__(self) -> str:
        return self.__key
