from apparser.debuggers.base import BaseDebugger

from apparser.exceptions import DebugException
from apparser.instructions import BaseInstruction


class Debugger(BaseDebugger):
    """Store executed instructions and wrap raised errors."""

    def __init__(self):
        """Initialize a debugger with an empty instruction log."""
        self.__instructions: list[BaseInstruction] = []

    def __form_log(self) -> str:
        result = ""
        for i in range(len(self.__instructions)):
            instruction = self.__instructions[i]
            result += f"\n{i}\t{instruction.id}\t{instruction.__class__.__name__}"
        return result

    def try_perform(self, instruction: BaseInstruction, *args, **kwargs):
        """Execute an instruction and convert failures to debug exceptions.

        :param instruction: Instruction to execute.
        :type instruction: BaseInstruction
        :param args: Positional arguments passed to the instruction.
        :param kwargs: Keyword arguments passed to the instruction.
        :raises DebugException: If the instruction raises an exception.
        """
        try:
            self.__instructions.append(instruction)
            instruction.perform(*args, **kwargs)
        except DebugException as e:
            result = self.__form_log().join(["\t" + i for i in str(e).split("\n")])
            raise DebugException(result)
        except Exception as e:
            formed_log = self.__form_log()
            max_string_len = max([len(i) for i in formed_log.split("\n")])
            raise_text = f'{formed_log}\n{max_string_len * "-"}\n{e}'
            raise DebugException(raise_text)

    def clear_contex(self):
        """Clear the stored instruction log."""
        self.__instructions = []
