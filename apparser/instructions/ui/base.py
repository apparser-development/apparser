import abc

from apparser.core import BaseUi
from apparser.instructions.base import BaseInstruction


class UiInstruction(BaseInstruction):
    @property
    @abc.abstractmethod
    def id(self) -> int:
        pass

    @abc.abstractmethod
    def perform(self, ui: BaseUi, *args, **kwargs):
        pass
