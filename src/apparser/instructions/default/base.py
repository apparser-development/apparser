import abc

from apparser.base.ui import Ui


class Instruction(abc.ABC):
    @abc.abstractmethod
    def __call__(self, ui: Ui):
        pass
