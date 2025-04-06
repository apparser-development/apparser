from apparser.base import Ui, App
from apparser.instructions.algorithms.base import Algorithm
from apparser.instructions.default.base import Instruction


class DefaultAlgorithm(Algorithm):
    def __init__(self, instructions: list[Instruction]):
        self.__instructions = instructions

    def perform(self, ui: Ui, *args, **kwargs):
        ui.window.to_main()
        for instruction in self.__instructions:
            instruction.perform(ui)

    @property
    def instructions(self) -> list[Instruction]:
        return self.__instructions
