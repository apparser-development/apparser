import abc

from apparser.core import Ui


class Instruction(abc.ABC):
    @abc.abstractmethod
    def perform(self, ui: Ui, *args, **kwargs):
        pass
