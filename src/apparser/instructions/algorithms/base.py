import abc

from apparser.instructions.default.base import Instruction


class Algorithm(Instruction, abc.ABC):
    @property
    @abc.abstractmethod
    def instructions(self):
        pass