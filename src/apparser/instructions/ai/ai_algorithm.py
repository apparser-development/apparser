from apparser.ai_readers.base import AiReader
from apparser.base import Ui
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.default.base import Instruction


class AiInstructionsAlgorithm(AiInstruction):
    def __init__(self, instructions: list[AiInstruction | Instruction]):
        self.__instructions = instructions

    def __call__(self, ui: Ui, ai_reader: AiReader):
        for instruction in self.__instructions:
            if isinstance(instruction, AiInstruction):
                instruction(ui, ai_reader)
            elif isinstance(instruction, Instruction):
                instruction(ui)
            else:
                raise ValueError(f'Unexpected instruction type: {type(instruction)}')
