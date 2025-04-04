import abc

from apparser.instructions.default.base import Instruction


class Algorithm(Instruction, abc.ABC):
    @abc.abstractmethod
    @property
    def instructions(self):
        pass