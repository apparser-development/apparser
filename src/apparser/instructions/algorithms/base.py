import abc

from apparser.instructions.default.base import Instruction


class Algorithm(Instruction, abc.ABC):
    @abc.abstractmethod
    def add_instruction(self, instruction):
        pass

    @property
    @abc.abstractmethod
    def instructions(self):
        pass
