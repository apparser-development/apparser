import abc

from apparser.core import BaseUi
from apparser.text_readers import BaseTextReader
from apparser.instructions.base import BaseInstruction


class SpeakInstruction(BaseInstruction):
    @property
    @abc.abstractmethod
    def id(self) -> int:
        pass

    @abc.abstractmethod
    def perform(self, ui: BaseUi, ai_reader: BaseTextReader, *args, **kwargs) -> BaseUi:
        pass