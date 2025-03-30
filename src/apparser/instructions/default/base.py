import abc

from apparser.base import Ui


class Instruction(abc.ABC):
    @abc.abstractmethod
    def __call__(self, ui: Ui, *args, **kwargs):
        pass
