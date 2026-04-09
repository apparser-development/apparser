from apparser.core import Ui
from apparser.algorithms.base import BaseAlgorithm
from apparser.instructions.base import Instruction


class NamesAlgorithm(BaseAlgorithm):
    def __init__(self, instructions: list[str]):
        self.__instructions = instructions

    def perform(self, ui: Ui, *args, **kwargs):
        pass

    def add_instruction(self, instruction: str):
        if not isinstance(instruction, str):
            raise TypeError(f"{instruction} must be str")

        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[str]:
        return self.__instructions
