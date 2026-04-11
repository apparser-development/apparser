import abc


class BaseInstruction(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def id(self) -> int:
        pass

    @abc.abstractmethod
    def perform(self, *args, **kwargs):
        pass