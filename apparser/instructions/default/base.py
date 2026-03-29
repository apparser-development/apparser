import abc

from apparser.core import WindowUi


class Instruction(abc.ABC):
    @abc.abstractmethod
    def perform(self, ui: WindowUi, *args, **kwargs):
        pass
