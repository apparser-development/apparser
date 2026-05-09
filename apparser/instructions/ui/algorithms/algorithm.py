from apparser.instructions.base import BaseInstruction
from apparser.instructions.ui.algorithms.base import BaseAlgorithm

from apparser.core import BaseUi
from apparser.instructions.debuggers import BaseDebugger
from apparser.instructions.debuggers import Debugger


class Algorithm(BaseAlgorithm):
    """Run UI instructions sequentially for a single window context."""

    def __init__(self, instructions: list[BaseInstruction],
                 debugger: BaseDebugger | None | bool = None):
        """Initialize a UI instruction algorithm.

        :param instructions: UI instructions or default instructions to execute in order.
        :type instructions: list[BaseInstruction]
        :param debugger: Debugger used to wrap instruction execution.
        :type debugger: BaseDebugger | None
        :raises TypeError: If ``debugger`` has an invalid type.
        """
        if debugger is None or debugger is True:
            debugger = Debugger()

        if debugger is False:
            debugger = None

        if debugger is not None and not isinstance(debugger, BaseDebugger):
            raise TypeError("debugger must be BaseDebugger or None")

        self.__instructions = instructions
        self.__debugger = debugger

    @property
    def id(self) -> int:
        return 1500

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.to_foreground()
        if self.__debugger is not None:
            self.__debugger.clear_context()

        for instruction in self.__instructions:
            if not isinstance(instruction, BaseInstruction) or instruction.id > 1999:
                raise TypeError(f"{instruction} must be BaseInstruction or UiInstruction")

            if self.__debugger is not None:
                self.__debugger.try_perform(instruction, ui)
            else:
                instruction.perform(ui)

    def add_instruction(self, instruction: BaseInstruction):
        if not isinstance(instruction, BaseInstruction) or instruction.id > 1999:
            raise TypeError(f"{instruction} must be BaseInstruction or UiInstruction")

        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[BaseInstruction]:
        return self.__instructions
