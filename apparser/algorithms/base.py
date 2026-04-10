import abc

from apparser.core import BaseUi


class BaseAlgorithm(abc.ABC):
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