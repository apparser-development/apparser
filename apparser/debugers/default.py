from logging import Logger, getLogger

from apparser.debugers.base import BaseDebugger

from apparser.core import BaseUi
from apparser.exceptions import DebugException
from apparser.instructions import Instruction
from apparser.instructions.ai import AiInstruction


class Debugger(BaseDebugger):
    def __init__(self):
        self.__instructions: list[Instruction | AiInstruction] = []

    def __form_log(self) -> str:
        result = ""
        for instruction in self.__instructions:
            result += f"{instruction.id}\t{instruction.name}\n"
        return result

    def try_perform(self, instruction: Instruction | AiInstruction, *args, **kwargs):
        try:
            self.__instructions.append(instruction)
            instruction.perform(*args, **kwargs)
        except DebugException as e:
            result = self.__form_log().join(["\t" + i for i in str(e).split("\n")])
            raise DebugException(result)
        except Exception as e:
            formed_log = self.__form_log()
            max_string_len = max([len(i) for i in formed_log.split("\n")])
            raise_text = f"{formed_log}{max_string_len * "-"}\n{e}"
            raise DebugException(raise_text)
