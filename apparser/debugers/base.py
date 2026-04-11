import abc

from apparser.instructions import Instruction
from apparser.instructions.ai import AiInstruction


class BaseDebugger(abc.ABC):
    @abc.abstractmethod
    def clear_contex(self):
        pass

    @abc.abstractmethod
    def try_perform(self, instruction: Instruction | AiInstruction, *args, **kwargs):
        pass
