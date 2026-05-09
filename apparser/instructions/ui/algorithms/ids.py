from typing import Any

from apparser.core import BaseUi
from apparser.instructions.debuggers import BaseDebugger, Debugger
from apparser.instructions.ui.algorithms.base import BaseAlgorithm
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
    """Resolve and execute instructions by their numeric identifiers."""

    def __init__(self, instructions: list[tuple[int, list[Any]]], debugger: BaseDebugger | bool = True):
        """Initialize an identifier-based instruction algorithm.

        :param instructions: Sequence of instruction identifiers with their arguments.
        :type instructions: list[tuple[int, list[Any]]]
        :param debugger: Debugger used to wrap instruction execution. If True, use Debugger. If False do not wrap instruction execution.
        :type debugger: BaseDebugger | bool
        :raises TypeError: If ``debugger`` has an invalid type.
        """

        if not isinstance(debugger, BaseDebugger) and not isinstance(debugger, bool):
            raise TypeError(f"debugger must be a bool or BaseDebugger")

        if debugger == True:
            debugger = Debugger()

        elif debugger == False:
            debugger = None

        self.__debugger = debugger
        self.__instructions = instructions

    @property
    def id(self) -> int:
        return 1501

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.to_foreground()

        if self.__debugger is not None:
            self.__debugger.clear_context()

        for instruction_data in self.__instructions:
            instruction_id, instruction_args = _check_instruction(instruction_data)

            instruction = get_instruction_by_id(instruction_id)
            if instruction is None:
                raise ValueError(f"instruction with id {instruction_id} not found")
            
            instruction = instruction(*instruction_args)
            if self.__debugger is not None:
                self.__debugger.try_perform(instruction, ui, *args, **kwargs)
            else:
                instruction.perform(ui, *args, **kwargs)

    def add_instruction(self, instruction: tuple[int, list[Any]]):
        _check_instruction(instruction)
        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[tuple[int, list[Any]]]:
        return self.__instructions
