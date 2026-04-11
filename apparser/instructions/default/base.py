import abc

from apparser.core import BaseUi
from apparser.instructions.base import BaseInstruction


class Instruction(BaseInstruction):
    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    @abc.abstractmethod
    def id(self) -> int:
        pass

    @abc.abstractmethod
    def perform(self, ui: BaseUi, *args, **kwargs):
        pass
