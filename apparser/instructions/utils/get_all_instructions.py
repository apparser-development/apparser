import inspect

from apparser.instructions import ocr, default, speak, ui
from apparser.instructions.base import BaseInstruction


def get_all_instructions() -> list[type[BaseInstruction]]:
    """Collect all concrete instruction classes from instruction modules.

    :return: Collected concrete instruction classes.
    :rtype: list[type[BaseInstruction]]
    """
    result = []
    for module in [default, ocr, speak, ui]:
        for instruction_name in module.__all__:
            instruction = getattr(module, instruction_name)
            if (inspect.isclass(instruction)
                    and issubclass(instruction, BaseInstruction)
                    and not inspect.isabstract(instruction)):
                result.append(instruction)
    return result
