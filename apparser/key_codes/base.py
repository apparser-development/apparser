import abc


class BaseKeyCode(abc.ABC):
    @abc.abstractmethod
    def __str__(self) -> str:
        pass