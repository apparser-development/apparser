from typing import Any

from apparser.core import BaseUi
from apparser.debuggers import BaseDebugger, Debugger
from apparser.instructions.algorithms.base import BaseAlgorithm
from apparser.instructions.utils import get_instruction_by_name


def _check_instruction(instruction: tuple[str, list[Any]]) -> tuple[str, list[Any]]:
    if not isinstance(instruction, tuple):
        raise TypeError(f"{instruction} must be tuple")

    instruction_name, instruction_args = instruction
    if not isinstance(instruction_name, str):
        raise TypeError(f"{instruction_name} must be str")

    if not isinstance(instruction_args, list):
        raise TypeError(f"{instruction_args} must be list")

    return instruction_name, instruction_args


class NamesAlgorithm(BaseAlgorithm):
    def __init__(self, instructions: list[tuple[str, list[Any]]], debugger: BaseDebugger | None = Debugger()):
        if debugger is not None and not isinstance(debugger, BaseDebugger):
            raise TypeError("debugger must be BaseDebugger or None")
        
        self.__debugger = debugger
        self.__instructions = instructions

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.to_foreground()
        for instruction_data in self.__instructions:
            instruction_name, instruction_args = _check_instruction(instruction_data)

            instruction_type = get_instruction_by_name(instruction_name)
            if instruction_type is None:
                raise ValueError(f"instruction with name {instruction_name} not found")
            
            instruction = instruction_type(*instruction_args)
            if self.__debugger is not None:
                self.__debugger.try_perform(instruction, ui, *args, **kwargs)
            else:
                instruction.perform(ui, *args, **kwargs)

    def add_instruction(self, instruction: tuple[str, list[Any]]):
        _check_instruction(instruction)
        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[tuple[str, list[Any]]]:
        return self.__instructions
