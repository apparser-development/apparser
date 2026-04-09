import abc

from apparser.core import Ui


class Instruction(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> str: 
        pass

    @property
    @abc.abstractmethod
    def id(self) -> int: 
        pass

    @abc.abstractmethod
    def perform(self, ui: Ui, *args, **kwargs):
        pass
