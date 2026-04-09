import abc

from apparser.core import Ui


class Instruction(abc.ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    @abc.abstractmethod
    def id(self) -> int:
        pass

    @abc.abstractmethod
    def perform(self, ui: Ui, *args, **kwargs):
        pass
