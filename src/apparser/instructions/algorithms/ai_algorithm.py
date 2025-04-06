from apparser.ai_readers.base import AiReader
from apparser.ai_readers.readers.easy_ocr import EasyOcrReader
from apparser.base import Ui, App
from apparser.instructions.ai.base import AiInstruction
from apparser.ai_readers.readers.screens_controller import ScreensController
from apparser.instructions.algorithms.base import Algorithm
from apparser.instructions.default.base import Instruction


class AiAlgorithm(Algorithm):
    def __init__(self,
                 instructions: list[AiInstruction | Instruction],
                 ai_reader: AiReader = ScreensController(EasyOcrReader())):
        self.__instructions = instructions
        self.__ai_reader = ai_reader

    def perform(self, ui: Ui, *args, **kwargs):
        ui.window.to_main()
        for instruction in self.__instructions:
            instruction.perform(ui, self.__ai_reader)

    @property
    def instructions(self) -> list[AiInstruction | Instruction]:
        return self.__instructions
