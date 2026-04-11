from apparser.core import BaseUi
from apparser.debugers import BaseDebugger, Debugger
from apparser.instructions.ai.base import AiInstruction
from apparser.algorithms.base import BaseAlgorithm
from apparser.instructions.default.base import Instruction
from apparser.text_readers import BaseTextReader, EasyOcrReader, ScreensController


class AiAlgorithm(BaseAlgorithm):
    def __init__(self,
                 instructions: list[AiInstruction | Instruction],
                 ai_reader: BaseTextReader = ScreensController(EasyOcrReader()),
                 debuger: BaseDebugger | None = Debugger()):
        
        self.__instructions = instructions
        self.__ai_reader = ai_reader
        self.__debugger = debuger

    def perform(self, ui: BaseUi, *args, **kwargs):
        if self.__debugger is not None:
            self.__debugger.clear_contex()

        ui.window.to_foreground()
        for instruction in self.__instructions:
            if not (isinstance(instruction, Instruction) or isinstance(instruction, AiInstruction)):
                raise TypeError(f"{instruction} must be Instruction or AiInstruction")
            
            if self.__debugger is not None:
                self.__debugger.try_perform(instruction, ui, self.__ai_reader)
            else:
                instruction.perform(ui, self.__ai_reader)

    def add_instruction(self, instruction: Instruction | AiInstruction):
        if not (isinstance(instruction, Instruction) or isinstance(instruction, AiInstruction)):
            raise TypeError(f"{instruction} must be Instruction or AiInstruction")

        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[AiInstruction | Instruction]:
        return self.__instructions
