import abc

from apparser.core import BaseUi
from apparser.instructions.base import BaseInstruction

class BaseAlgorithm(BaseInstruction):
    @property
    @abc.abstractmethod
    def id(self):
        pass

    @abc.abstractmethod
    def add_instruction(self, instruction):
        pass

    @property
    @abc.abstractmethod
    def instructions(self):
        pass

    @abc.abstractmethod
    def perform(self, ui: BaseUi, *args, **kwargs):
        pass