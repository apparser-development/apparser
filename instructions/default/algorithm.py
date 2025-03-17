from base import Ui
from instructions.default.base import Instruction


class InstructionsAlgorithm(Instruction):
    def __init__(self, instructions: list[Instruction]):
        self.__instructions = instructions

    def __call__(self, ui: Ui):
        for instruction in self.__instructions:
            instruction(ui)
