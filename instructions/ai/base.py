import abc

from ai_readers.base import AiReader
from base.ui import Ui


class AiInstruction(abc.ABC):
    @abc.abstractmethod
    def perform(self, ui: Ui, ai: AiReader):
        pass
