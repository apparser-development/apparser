from typing import Any
import inspect

from apparser.core import BaseUi

from apparser.instructions.debuggers import BaseDebugger, Debugger
from apparser.instructions.ui.algorithms.base import BaseAlgorithm
from apparser.instructions.base import BaseInstruction


class UniqueAlgorithm(BaseAlgorithm):
    """Run instructions with arguments resolved from unique attribute types."""

    def __init__(self,
                 instructions: list[BaseInstruction],
                 attributes: list[Any],
                 debugger: BaseDebugger | bool = True):
        """Initialize an algorithm that injects attributes into instructions.

        :param instructions: Instructions to execute in order.
        :type instructions: list[BaseInstruction]
        :param attributes: Attribute values matched to instruction parameters by type.
        :type attributes: list[Any]
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

        attributes.reverse()

        self.__instructions = instructions
        self.__attributes = attributes
        self.__debugger = debugger

    def __form_args(self, instruction: BaseInstruction) -> dict[str, Any]:
        result = {}
        function_signature = inspect.signature(instruction.perform)
        for arg in function_signature.parameters.values():
            for a in self.__attributes:
                if arg.annotation is type(a):
                    result[arg.name] = a
        return result

    @property
    def id(self) -> int:
        return 1505

    def perform(self, ui: BaseUi, *args, **kwargs):
        if self.__debugger is not None:
            self.__debugger.clear_context()

        ui.window.to_foreground()
        for instruction in self.__instructions:
            if not (isinstance(instruction, BaseInstruction)):
                raise TypeError(f"{instruction} must be BaseInstruction")

            instruction_kwargs = self.__form_args(instruction)

            if self.__debugger is not None:
                self.__debugger.try_perform(instruction, ui, **instruction_kwargs)
            else:
                instruction.perform(ui, **instruction_kwargs)

    def add_instruction(self, instruction: BaseInstruction):
        if not (isinstance(instruction, BaseInstruction)):
            raise TypeError(f"{instruction} must be BaseInstruction")

        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[BaseInstruction]:
        return self.__instructions
