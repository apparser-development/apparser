from apparser.core import BaseUi

from apparser.speakers import BaseSpeaker, ChatTTSSpeaker

from apparser.instructions.debuggers import BaseDebugger, Debugger
from apparser.instructions.ui.algorithms.base import BaseAlgorithm
from apparser.instructions.base import BaseInstruction
from apparser.instructions.speak.base import SpeakInstruction


class SpeakAlgorithm(BaseAlgorithm):
    """Run instruction sequences that depend on a speaker backend."""

    def __init__(self,
                 instructions: list[BaseInstruction],
                 speaker: BaseSpeaker | None = None,
                 debugger: BaseDebugger | bool = True):
        """Initialize a speech-oriented instruction algorithm.

        :param instructions: Instructions to execute in order.
        :type instructions: list[BaseInstruction]
        :param speaker: Speaker used during execution.
        :type speaker: BaseSpeaker | None
        :param debugger: Debugger used to wrap instruction execution. If True, use Debugger. If False do not wrap instruction execution.
        :type debugger: BaseDebugger | bool
        :raises TypeError: If ``speaker`` or ``debugger`` has an invalid type.
        """
        if speaker is None:
            speaker = ChatTTSSpeaker()

        if not isinstance(speaker, BaseSpeaker):
            raise TypeError("speaker must be BaseSpeaker")

        if not isinstance(debugger, BaseDebugger) and not isinstance(debugger, bool):
            raise TypeError(f"debugger must be a bool or BaseDebugger")

        if debugger == True:
            debugger = Debugger()

        elif debugger == False:
            debugger = None

        self.__instructions = instructions
        self.__speaker = speaker
        self.__debugger = debugger

    def __perform(self, instruction: BaseInstruction, *args):
        if self.__debugger is not None:
            self.__debugger.try_perform(instruction, *args)
        else:
            instruction.perform(*args)

    @property
    def id(self) -> int:
        return 1504

    def perform(self, ui: BaseUi, *args, **kwargs):
        if self.__debugger is not None:
            self.__debugger.clear_context()

        ui.window.to_foreground()
        for instruction in self.__instructions:
            if not (isinstance(instruction, BaseInstruction)):
                raise TypeError(f"{instruction} must be BaseInstruction")

            if isinstance(instruction, SpeakInstruction):
                self.__perform(instruction, self.__speaker)
            elif isinstance(instruction, BaseInstruction):
                self.__perform(instruction, ui)

    def add_instruction(self, instruction: BaseInstruction):
        if not (isinstance(instruction, BaseInstruction)):
            raise TypeError(f"{instruction} must be BaseInstruction")

        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[BaseInstruction]:
        return self.__instructions
