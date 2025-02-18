from ai_readers.base import AiReader
from base.app import App
from instructions.ai.base import AiInstruction
from instructions.default.base import Instruction
from performers.base import BasePerformer


class AiPerformer(BasePerformer):
    def __init__(self, app: App, ai_reader: AiReader):
        super().__init__(app)
        self.__ai_reader = ai_reader

    def perform(self, command: Instruction | AiInstruction):
        if command is Instruction:
            command.perform(self.app.ui)
        elif command is AiInstruction:
            command.perform(self.app.ui, self.__ai_reader)
        else:
            raise ValueError