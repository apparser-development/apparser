from apparser.core import WindowUi
from apparser.instructions.algorithm import BaseAlgorithm
from apparser.instructions.default.base import Instruction


class Algorithm(BaseAlgorithm):
    def __init__(self, instructions: list[Instruction]):
        self.__instructions = instructions

    def perform(self, ui: WindowUi, *args, **kwargs):
        ui.window.to_foreground()
        for instruction in self.__instructions:
            if not isinstance(instruction, Instruction):
                raise TypeError(f"{instruction} must be Instruction")
            instruction.perform(ui)

    def add_instruction(self, instruction: Instruction):
        if not isinstance(instruction, Instruction):
            raise TypeError(f"{instruction} must be Instruction")

        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[Instruction]:
        return self.__instructions
