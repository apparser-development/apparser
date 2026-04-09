from logging import Logger, getLogger

from apparser.core import Ui
from apparser.debugers.base import Debugger
from apparser.instructions import Instruction


class DefaultDebugger(Debugger):
    @classmethod
    def create(cls, ui: Ui, logger: Logger = getLogger(__name__)):
        cls.__ui = ui
        cls.__instructions: list[Instruction] = []
        return cls()

    def __form_log(self) -> str:
        result = ""
        for instruction in self.__instructions:
            result += f"{instruction.id}\t{instruction.name}\n"
        return result

    def perform(self, instruction: Instruction):
        try:
            instruction.perform(self.__ui)
        except Exception as e:
            raise e

