import abc

from apparser.instructions import BaseInstruction


class BaseDebugger(abc.ABC):
    @abc.abstractmethod
    def clear_contex(self):
        pass

    @abc.abstractmethod
    def try_perform(self, instruction: BaseInstruction, *args, **kwargs):
        pass
