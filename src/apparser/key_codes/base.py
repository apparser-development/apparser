import abc


class KeyCode(abc.ABC):
    @property
    @abc.abstractmethod
    def key(self) -> str:
        pass