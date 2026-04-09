from apparser.core import Ui
from apparser.algorithms.base import BaseAlgorithm
from apparser.instructions.base import Instruction


class IdsAlgorithm(BaseAlgorithm):
    def __init__(self, instructions: list[int]):
        self.__instructions = instructions

    def perform(self, ui: Ui, *args, **kwargs):
        pass

    def add_instruction(self, instruction: int):
        if not isinstance(instruction, int):
            raise TypeError(f"{instruction} must be int")

        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[str]:
        return self.__instructions
