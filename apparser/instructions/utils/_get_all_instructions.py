import inspect

from apparser.instructions import ai, default
from apparser.instructions.ui.base import UiInstruction
from apparser.instructions.ai.base import AiInstruction


def _get_all_instructions() -> list[type[UiInstruction | AiInstruction]]:
    result = []
    for module in [default, ai]:
        for instruction_name in module.__all__:
            instruction = getattr(module, instruction_name)
            if (inspect.isclass(instruction)
                    and issubclass(instruction, UiInstruction)
                    and not inspect.isabstract(instruction)):
                result.append(instruction)
    return result
