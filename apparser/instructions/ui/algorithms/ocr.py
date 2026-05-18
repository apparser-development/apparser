from apparser.core import BaseUi

from apparser.text_readers import BaseTextReader, EasyOcrReader, ScreensController

from apparser.instructions.debuggers import BaseDebugger, Debugger
from apparser.instructions.ui.algorithms.base import BaseAlgorithm
from apparser.instructions.base import BaseInstruction


class OCRAlgorithm(BaseAlgorithm):
    """Run instruction sequences that depend on OCR data."""

    def __init__(self,
                 instructions: list[BaseInstruction],
                 text_reader: BaseTextReader | None = None,
                 debugger: BaseDebugger | bool = True):
        """Initialize an OCR-oriented instruction algorithm.

        :param instructions: Instructions to execute in order.
        :type instructions: list[BaseInstruction]
        :param text_reader: Text reader used during execution.
        :type text_reader: BaseTextReader | None
        :param debugger: Debugger used to wrap instruction execution. If True, use Debugger. If False do not wrap instruction execution.
        :type debugger: BaseDebugger | bool
        :raises TypeError: If ``text_reader`` or ``debugger`` has an invalid type.
        """
        if text_reader is None:
            text_reader = ScreensController(EasyOcrReader())

        if not isinstance(text_reader, BaseTextReader):
            raise TypeError("text_reader must be BaseTextReader")
        
        if not isinstance(debugger, BaseDebugger) and not isinstance(debugger, bool):
            raise TypeError(f"debugger must be a bool or BaseDebugger")

        if debugger == True:
            debugger = Debugger()

        elif debugger == False:
            debugger = None

        self.__instructions = instructions
        self.__text_reader = text_reader
        self.__debugger = debugger

    @property
    def id(self) -> int:
        return 1503

    def perform(self, ui: BaseUi, *args, **kwargs):
        if self.__debugger is not None:
            self.__debugger.clear_context()

        ui.window.to_foreground()
        for instruction in self.__instructions:
            if not (isinstance(instruction, BaseInstruction)):
                raise TypeError(f"{instruction} must be BaseInstruction")

            if self.__debugger is not None:
                self.__debugger.try_perform(instruction, ui, self.__text_reader)
            else:
                instruction.perform(ui, self.__text_reader)

    def add_instruction(self, instruction: BaseInstruction):
        if not (isinstance(instruction, BaseInstruction)):
            raise TypeError(f"{instruction} must be BaseInstruction")

        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[BaseInstruction]:
        return self.__instructions
