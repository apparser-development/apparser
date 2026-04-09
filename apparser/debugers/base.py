import abc

from apparser.core import Ui
from apparser.instructions import Instruction


class Debugger(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def create(cls, ui: Ui):
        pass

    @abc.abstractmethod
    def perform(self, instruction: Instruction):
        pass
