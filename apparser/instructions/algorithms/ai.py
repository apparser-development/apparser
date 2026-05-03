from apparser.core import BaseUi
from apparser.instructions.debuggers import BaseDebugger, Debugger
from apparser.instructions.algorithms.base import BaseAlgorithm
from apparser.instructions import BaseInstruction
from apparser.instructions.speak import SpeakInstruction
from apparser.instructions.ocr import OCRInstruction
from apparser.text_readers import BaseTextReader, EasyOcrReader, ScreensController
from apparser.speakers import BaseSpeaker, ChatTTSSpeaker


class AiAlgorithm(BaseAlgorithm):
    """Run mixed instruction sequences with OCR and speech dependencies."""

    def __init__(self,
                 instructions: list[BaseInstruction],
                 speaker: BaseSpeaker | None = None,
                 text_reader: BaseTextReader | None = None,
                 debugger: BaseDebugger | None = Debugger()):
        """Initialize an algorithm for mixed instruction pipelines.

        :param instructions: Instructions to execute in order.
        :type instructions: list[BaseInstruction]
        :param speaker: Speaker used for speech instructions.
        :type speaker: BaseSpeaker | None
        :param text_reader: Text reader used for OCR instructions.
        :type text_reader: BaseTextReader | None
        :param debugger: Debugger used to wrap instruction execution.
        :type debugger: BaseDebugger | None
        :raises TypeError: If ``text_reader``, ``speaker`` or ``debugger`` has an invalid type.
        """
        if speaker is None:
            speaker = ChatTTSSpeaker()

        if text_reader is None:
            text_reader = ScreensController(EasyOcrReader())

        if not isinstance(text_reader, BaseTextReader):
            raise TypeError("text_reader must be BaseTextReader")

        if not isinstance(speaker, BaseSpeaker):
            raise TypeError("text_reader must be BaseTextReader")

        if debugger is not None and not isinstance(debugger, BaseDebugger):
            raise TypeError("debugger must be BaseDebugger or None")

        self.__instructions = instructions
        self.__text_reader = text_reader
        self.__speaker = speaker
        self.__debugger = debugger

    @property
    def id(self) -> int:
        return 1000

    def perform(self, ui: BaseUi, *args, **kwargs):
        if self.__debugger is not None:
            self.__debugger.clear_contex()

        ui.window.to_foreground()
        for instruction in self.__instructions:
            if not (isinstance(instruction, BaseInstruction)):
                raise TypeError(f"{instruction} must be Instruction or AiInstruction")
            if isinstance(instruction, SpeakInstruction):
                if self.__debugger is not None:
                    self.__debugger.try_perform(instruction, ui, self.__speaker)
                else:
                    instruction.perform(ui, self.__speaker)
            elif isinstance(instruction, OCRInstruction):
                if self.__debugger is not None:
                    self.__debugger.try_perform(instruction, ui, self.__text_reader)
                else:
                    instruction.perform(ui, self.__text_reader)
            else:
                instruction.perform(ui)

    def add_instruction(self, instruction: BaseInstruction):
        if not (isinstance(instruction, BaseInstruction)):
            raise TypeError(f"{instruction} must be Instruction or AiInstruction")

        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[BaseInstruction]:
        return self.__instructions
