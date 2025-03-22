import abc
from apparser.ai_readers.base import AiReader
from apparser.base.ui import Ui


class AiInstruction(abc.ABC):
    @abc.abstractmethod
    def __call__(self, ui: Ui, ai: AiReader):
        pass

