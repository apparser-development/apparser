from apparser.instructions.algorithms.base import BaseAlgorithm

from apparser.core import BaseUi
from apparser.instructions.debuggers import BaseDebugger
from apparser.instructions.ui.base import UiInstruction


class Algorithm(BaseAlgorithm):
    """Run UI instructions sequentially for a single window context."""

    def __init__(self, instructions: list[UiInstruction],
                 debugger: BaseDebugger | None):
        """Initialize a UI instruction algorithm.

        :param instructions: UI instructions to execute in order.
        :type instructions: list[UiInstruction]
        :param debugger: Debugger used to wrap instruction execution.
        :type debugger: BaseDebugger | None
        :raises TypeError: If ``debugger`` has an invalid type.
        """
        if debugger is not None and not isinstance(debugger, BaseDebugger):
            raise TypeError("debugger must be BaseDebugger or None")

        self.__instructions = instructions
        self.__debugger = debugger

    @property
    def id(self) -> int:
        return 1001

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.to_foreground()
        if self.__debugger is not None:
            self.__debugger.clear_contex()

        for instruction in self.__instructions:
            if not isinstance(instruction, UiInstruction):
                raise TypeError(f"{instruction} must be Instruction")
            if self.__debugger is not None:
                self.__debugger.try_perform(instruction, ui)
            else:
                instruction.perform(ui)
                
    def add_instruction(self, instruction: UiInstruction):
        if not isinstance(instruction, UiInstruction):
            raise TypeError(f"{instruction} must be Instruction")

        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[UiInstruction]:
        return self.__instructions
