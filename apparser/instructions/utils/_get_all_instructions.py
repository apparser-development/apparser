import inspect

from apparser.instructions import ai, default
from apparser.instructions.base import Instruction


def _get_all_instructions() -> list[type[Instruction]]:
    result = []
    for module in [default, ai]:
        for instruction_name in module.__all__:
            instruction = getattr(module, instruction_name)
            if (inspect.isclass(instruction)
                    and issubclass(instruction, Instruction)
                    and not inspect.isabstract(instruction)):
                result.append(instruction)
    return result
