import abc

from apparser.core import BaseUi
from apparser.text_readers import BaseTextReader
from apparser.instructions.base import BaseInstruction

class AiInstruction(BaseInstruction):
    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    @abc.abstractmethod
    def id(self) -> int:
        pass

    @abc.abstractmethod
    def perform(self, ui: BaseUi, ai_reader: BaseTextReader, *args, **kwargs) -> BaseUi:
        pass