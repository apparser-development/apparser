import abc


class KeyCode(abc.ABC):
    @abc.abstractmethod
    def __str__(self) -> str:
        pass