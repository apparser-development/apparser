from apparser.core import BaseUi
from apparser.debuggers import BaseDebugger, Debugger
from apparser.algorithms.base import BaseAlgorithm
from apparser.instructions import BaseInstruction
from apparser.speakers import BaseSpeaker, ChatTTSSpeaker


class SpeakAlgorithm(BaseAlgorithm):
    def __init__(self,
                 instructions: list[BaseInstruction],
                 speaker: BaseSpeaker = ChatTTSSpeaker(),
                 debugger: BaseDebugger | None = Debugger()):
        if not isinstance(speaker, BaseSpeaker):
            raise TypeError("speaker must be BaseSpeaker")
        
        if debugger is not None and not isinstance(debugger, BaseDebugger):
            raise TypeError("debugger must be BaseDebugger or None")

        self.__instructions = instructions
        self.__speaker = speaker
        self.__debugger = debugger

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
