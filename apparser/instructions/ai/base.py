import abc

from apparser.text_readers import AiReader
from apparser.core import Ui
from apparser.instructions.base import Instruction


class AiInstruction(Instruction):
    @abc.abstractmethod
    def perform(self, ui: Ui, ai: AiReader):
        pass

