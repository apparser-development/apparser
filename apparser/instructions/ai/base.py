import abc
from apparser.text_readers import AiReader
from apparser.core import WindowUi


class AiInstruction(abc.ABC):
    @abc.abstractmethod
    def perform(self, ui: WindowUi, ai: AiReader):
        pass

