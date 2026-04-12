from apparser.debuggers.base import BaseDebugger

from apparser.exceptions import DebugException
from apparser.instructions import BaseInstruction


class Debugger(BaseDebugger):
    def __init__(self):
        self.__instructions: list[BaseInstruction] = []

    def __form_log(self) -> str:
        result = ""
        for i in range(len(self.__instructions)):
            instruction = self.__instructions[i]
            result += f"\n{i}\t{instruction.id}\t{instruction.name}"
        return result

    def try_perform(self, instruction: BaseInstruction, *args, **kwargs):
        try:
            self.__instructions.append(instruction)
            instruction.perform(*args, **kwargs)
        except DebugException as e:
            result = self.__form_log().join(["\t" + i for i in str(e).split("\n")])
            raise DebugException(result)
        except Exception as e:
            formed_log = self.__form_log()
            max_string_len = max([len(i) for i in formed_log.split("\n")])
            raise_text = f"{formed_log}\n{max_string_len * "-"}\n{e}"
            raise DebugException(raise_text)

    def clear_contex(self):
        self.__instructions = []