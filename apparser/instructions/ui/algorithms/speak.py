from apparser.core import BaseUi
from apparser.instructions.debuggers import BaseDebugger, Debugger
from apparser.instructions.ui.algorithms.base import BaseAlgorithm
from apparser.instructions.base import BaseInstruction
from apparser.speakers import BaseSpeaker, ChatTTSSpeaker


class SpeakAlgorithm(BaseAlgorithm):
    """Run instruction sequences that depend on a speaker backend."""

    def __init__(self,
                 instructions: list[BaseInstruction],
                 speaker: BaseSpeaker | None = None,
                 debugger: BaseDebugger | None | bool = None):
        """Initialize a speech-oriented instruction algorithm.

        :param instructions: Instructions to execute in order.
        :type instructions: list[BaseInstruction]
        :param speaker: Speaker used during execution.
        :type speaker: BaseSpeaker | None
        :param debugger: Debugger used to wrap instruction execution.
        :type debugger: BaseDebugger | None
        :raises TypeError: If ``speaker`` or ``debugger`` has an invalid type.
        """
        if speaker is None:
            speaker = ChatTTSSpeaker()

        if not isinstance(speaker, BaseSpeaker):
            raise TypeError("speaker must be BaseSpeaker")
        
        if debugger is None or debugger is True:
            debugger = Debugger()

        if debugger is False:
            debugger = None

        if debugger is not None and not isinstance(debugger, BaseDebugger):
            raise TypeError("debugger must be BaseDebugger or None")

        self.__instructions = instructions
        self.__speaker = speaker
        self.__debugger = debugger

    @property
    def id(self) -> int:
        return 1504

    def perform(self, ui: BaseUi, *args, **kwargs):
        if self.__debugger is not None:
            self.__debugger.clear_contex()

        ui.window.to_foreground()
        for instruction in self.__instructions:
            if not (isinstance(instruction, BaseInstruction)):
                raise TypeError(f"{instruction} must be Instruction or AiInstruction")
            
            if self.__debugger is not None:
                self.__debugger.try_perform(instruction, ui, self.__speaker)
            else:
                instruction.perform(ui, self.__speaker)

    def add_instruction(self, instruction: BaseInstruction):
        if not (isinstance(instruction, BaseInstruction)):
            raise TypeError(f"{instruction} must be Instruction or AiInstruction")

        self.__instructions.append(instruction)

    @property
    def instructions(self) -> list[BaseInstruction]:
        return self.__instructions
