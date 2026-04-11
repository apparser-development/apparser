from apparser.algorithms.base import BaseAlgorithm

from apparser.core import BaseUi
from apparser.debuggers import BaseDebugger
from apparser.instructions import Instruction


class Algorithm(BaseAlgorithm):
    def __init__(self, instructions: list[Instruction],
                 debugger: BaseDebugger | None):
        if debugger is not None and not isinstance(debugger, BaseDebugger):
            raise TypeError("debugger must be BaseDebugger or None")

        self.__instructions = instructions
        self.__debugger = debugger

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.to_foreground()
        if self.__debugger is not None:
            self.__debugger.clear_contex()

        for instruction in self.__instructions:
            if not isinstance(instruction, Instruction):
                raise TypeError(f"{instruction} must be Instruction")
            if self.__debugger is not None:
                self.__debugger.try_perform(instruction, ui)
            else:
                instruction.perform(ui)
                
    def add_instruction(self, instruction: Instruction):
        if not isinstance(instruction, Instruction):
            raise TypeError(f"{instruction} must be Instruction")

        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[Instruction]:
        return self.__instructions
