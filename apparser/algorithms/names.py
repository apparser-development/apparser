from typing import Any

from apparser.core import Ui
from apparser.algorithms.base import BaseAlgorithm
from apparser.instructions.utils import get_instruction_by_name


class NamesAlgorithm(BaseAlgorithm):
    def __init__(self, instructions: list[tuple[str, list[Any]]]):
        self.__instructions = instructions

    def __check_instruction(self, instruction: tuple[str, list[Any]]) -> tuple[str, list[Any]]:
        if not isinstance(instruction, tuple):
            raise TypeError(f"{instruction} must be tuple")

        instruction_name, instruction_args = instruction
        if not isinstance(instruction_name, str):
            raise TypeError(f"{instruction_name} must be str")

        if not isinstance(instruction_args, list):
            raise TypeError(f"{instruction_args} must be list")

        return instruction_name, instruction_args

    def perform(self, ui: Ui, *args, **kwargs):
        ui.window.to_foreground()
        for instruction_data in self.__instructions:
            instruction_name, instruction_args = self.__check_instruction(instruction_data)

            instruction = get_instruction_by_name(instruction_name)
            if instruction is None:
                raise ValueError(f"instruction with name {instruction_name} not found")

            instruction(*instruction_args).perform(ui, *args, **kwargs)

    def add_instruction(self, instruction: tuple[str, list[Any]]):
        self.__check_instruction(instruction)
        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[tuple[str, list[Any]]]:
        return self.__instructions
