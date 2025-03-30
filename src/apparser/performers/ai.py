from apparser.ai_readers.base import AiReader
from apparser.ai_readers.readers.easy_ocr import EasyOcrReader
from apparser.base import App
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.default.base import Instruction
from apparser.performers.base import BasePerformer


class AiPerformer(BasePerformer):
    def __init__(self, app: App, ai_reader: AiReader = EasyOcrReader()):
        super().__init__(app)
        self.__ai_reader = ai_reader

    def perform(self, command: Instruction | AiInstruction):
        if not isinstance(command, Instruction) or not isinstance(command, AiInstruction):
            raise ValueError()

        self.app.ui.window.to_main()
        command(self.app.ui, self.__ai_reader)

