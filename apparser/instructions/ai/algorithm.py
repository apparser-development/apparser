from apparser.core import Ui
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.algorithm import BaseAlgorithm
from apparser.instructions.default.base import Instruction
from apparser.text_readers.base import AiReader
from apparser.text_readers.easy_ocr import EasyOcrReader
from apparser.text_readers.screens_controller import ScreensController


class AiAlgorithm(BaseAlgorithm):
    def __init__(self,
                 instructions: list[AiInstruction | Instruction],
                 ai_reader: AiReader = ScreensController(EasyOcrReader())):
        self.__instructions = instructions
        self.__ai_reader = ai_reader

    def perform(self, ui: Ui, *args, **kwargs):
        ui.window.to_foreground()
        for instruction in self.__instructions:
            if not (isinstance(instruction, Instruction) or isinstance(instruction, AiInstruction)):
                raise TypeError(f"{instruction} must be Instruction or AiInstruction")
            instruction.perform(ui, self.__ai_reader)

    def add_instruction(self, instruction: Instruction | AiInstruction):
        if not (isinstance(instruction, Instruction) or isinstance(instruction, AiInstruction)):
            raise TypeError(f"{instruction} must be Instruction or AiInstruction")

        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[AiInstruction | Instruction]:
        return self.__instructions
