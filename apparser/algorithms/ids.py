from typing import Any

from apparser.core import BaseUi
from apparser.algorithms.base import BaseAlgorithm
from apparser.instructions.utils import get_instruction_by_id


def _check_instruction(instruction: tuple[int, list[Any]]) -> tuple[int, list[Any]]:
    if not isinstance(instruction, tuple):
        raise TypeError(f"{instruction} must be tuple")

    instruction_id, instruction_args = instruction
    if not isinstance(instruction_id, int):
        raise TypeError(f"{instruction_id} must be int")

    if not isinstance(instruction_args, list):
        raise TypeError(f"{instruction_args} must be list")

    return instruction_id, instruction_args


class IdsAlgorithm(BaseAlgorithm):
    def __init__(self, instructions: list[tuple[int, list[Any]]]):
        self.__instructions = instructions

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.to_foreground()
        for instruction_data in self.__instructions:
            instruction_id, instruction_args = _check_instruction(instruction_data)

            instruction = get_instruction_by_id(instruction_id)
            if instruction is None:
                raise ValueError(f"instruction with id {instruction_id} not found")

            instruction(*instruction_args).perform(ui, *args, **kwargs)

    def add_instruction(self, instruction: tuple[int, list[Any]]):
        _check_instruction(instruction)
        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[tuple[int, list[Any]]]:
        return self.__instructions
