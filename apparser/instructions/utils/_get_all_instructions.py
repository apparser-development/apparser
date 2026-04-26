import inspect

from apparser.instructions import ocr, default, speak, ui, algorithms
from apparser.instructions.base import BaseInstruction


def _get_all_instructions() -> list[type[BaseInstruction]]:
    result = []
    for module in [default, ocr, speak, ui, algorithms]:
        for instruction_name in module.__all__:
            instruction = getattr(module, instruction_name)
            if (inspect.isclass(instruction)
                    and issubclass(instruction, BaseInstruction)
                    and not inspect.isabstract(instruction)):
                result.append(instruction)
    return result
