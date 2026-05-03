import abc

from apparser.instructions.base import BaseInstruction


class BaseDebugger(abc.ABC):
    """Define the common interface for debugger implementations."""

    @abc.abstractmethod
    def clear_contex(self):
        """Clear the stored debugging context."""
        pass

    @abc.abstractmethod
    def try_perform(self, instruction: BaseInstruction, *args, **kwargs):
        """Execute an instruction with debugging support.

        :param instruction: Instruction to execute.
        :type instruction: BaseInstruction
        :param args: Positional arguments passed to the instruction.
        :param kwargs: Keyword arguments passed to the instruction.
        """
        pass
