import abc
from apparser.text_readers import AiReader
from apparser.core import Ui


class AiInstruction(abc.ABC):
    @abc.abstractmethod
    def perform(self, ui: Ui, ai: AiReader):
        pass

