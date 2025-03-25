from functools import singledispatchmethod

from apparser.ai_readers.base import AiReader
from apparser.ai_readers.readers.easy_ocr import EasyOcrReader
from apparser.base.app import App
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.default.base import Instruction
from apparser.performers.base import BasePerformer


class AiPerformer(BasePerformer):
    def __init__(self, app: App, ai_reader: AiReader = EasyOcrReader()):
        super().__init__(app)
        self.__ai_reader = ai_reader

    @singledispatchmethod
    def perform(self, command: Instruction | AiInstruction):
        raise NotImplementedError()

    @perform.register(Instruction)
    def _(self, command: Instruction):
        self.app.ui.to_main()
        command(self.app.ui)

    @perform.register(AiInstruction)
    def _(self, command: AiInstruction):
        self.app.ui.to_main()
        command(self.app.ui, self.__ai_reader)
