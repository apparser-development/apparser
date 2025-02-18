from ai_readers.base import AiReader
from base import Ui
from instructions.ai.base import AiInstruction


class ClickOnText(AiInstruction):
    def __init__(self, text: str):
        self.__text = text

    def perform(self, ui: Ui, ai: AiReader):
        pass
