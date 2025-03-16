from functools import singledispatchmethod

from ai_readers.base import AiReader
from base.app import App
from instructions.ai.base import AiInstruction
from instructions.default.base import Instruction
from performers.base import BasePerformer


class AiPerformer(BasePerformer):
    def __init__(self, app: App, ai_reader: AiReader):
        super().__init__(app)
        self.__ai_reader = ai_reader

    @singledispatchmethod
    def perform(self, command: Instruction | AiInstruction):
        raise NotImplementedError()

    @perform.register(Instruction)
    def _(self, command: Instruction):
        command(self.app.ui)

    @perform.register(AiInstruction)
    def _(self, command: AiInstruction):
        command(self.app.ui, self.__ai_reader)
