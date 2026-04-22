import abc


class BaseInstruction(abc.ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    @abc.abstractmethod
    def id(self) -> int:
        pass

    @abc.abstractmethod
    def perform(self, *args, **kwargs):
        pass