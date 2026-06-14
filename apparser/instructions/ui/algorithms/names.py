import inspect
from types import UnionType
from typing import Any, Union, get_args, get_origin

from apparser.core import BaseUi

from apparser.instructions import BaseInstruction
from apparser.instructions.debuggers import BaseDebugger, Debugger
from apparser.instructions.ui.algorithms.base import BaseAlgorithm
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


def _is_annotation_matches(annotation: Any, value: Any) -> bool:
    if annotation is inspect.Parameter.empty:
        return False

    if annotation is Any:
        return True

    annotation_origin = get_origin(annotation)
    annotation_args = get_args(annotation)
    if annotation_origin in (Union, UnionType):
        return any(_is_annotation_matches(i, value) for i in annotation_args)

    if isinstance(annotation_origin, type):
        return isinstance(value, annotation_origin)

    if isinstance(annotation, type):
        return isinstance(value, annotation)

    return annotation is type(value)


class NamesAlgorithm(BaseAlgorithm):
    """Resolve and execute instructions by their registered names."""

    def __init__(self,
                 instructions: list[tuple[str, list[Any]]],
                 attributes: list[Any],
                 debugger: BaseDebugger | bool = True):
        """Initialize a name-based instruction algorithm.

        :param instructions: Sequence of instruction names with their arguments.
        :type instructions: list[tuple[str, list[Any]]]
        :param attributes: Attribute values matched to instruction parameters by type.
        :type attributes: list[Any]
        :param debugger: Debugger used to wrap instruction execution. If True, use Debugger. If False do not wrap instruction execution.
        :type debugger: BaseDebugger | bool
        :raises TypeError: If ``debugger`` has an invalid type.
        """
        if not isinstance(attributes, list):
            raise TypeError("attributes must be list")

        if not isinstance(instructions, list):
            raise TypeError("instructions must be list")

        if not isinstance(debugger, BaseDebugger) and not isinstance(debugger, bool):
            raise TypeError(f"debugger must be a bool or BaseDebugger")

        if debugger == True:
            debugger = Debugger()

        elif debugger == False:
            debugger = None

        self.__debugger = debugger
        self.__instructions = instructions
        self.__attributes = attributes

    @property
    def id(self) -> int:
        return 1502

    def __form_args(self, instruction: BaseInstruction, *additional_args) -> dict[str, Any]:
        result = {}
        function_signature = inspect.signature(instruction.perform)
        for arg in function_signature.parameters.values():
            for a in self.__attributes + list(additional_args):
                if _is_annotation_matches(arg.annotation, a):
                    result[arg.name] = a
        return result

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.to_foreground()

        if self.__debugger is not None:
            self.__debugger.clear_context()

        for instruction_data in self.__instructions:
            instruction_name, instruction_args = _check_instruction(instruction_data)

            instruction_type = get_instruction_by_name(instruction_name)
            if instruction_type is None:
                raise ValueError(f"instruction with name {instruction_name} not found")

            instruction = instruction_type(*instruction_args)

            perform_kwargs = self.__form_args(instruction, ui)

            if self.__debugger is not None:
                self.__debugger.try_perform(instruction, **perform_kwargs)
            else:
                instruction.perform(ui, **perform_kwargs)

    def add_instruction(self, instruction: tuple[str, list[Any]]):
        _check_instruction(instruction)
        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[tuple[str, list[Any]]]:
        return self.__instructions
