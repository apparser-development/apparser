import abc

from base.ui import Ui


class Instruction(abc.ABC):
    @abc.abstractmethod
    def perform(self, ui: Ui):
        pass
