import abc
from apparser.ai_readers.base import AiReader
from apparser.base.ui import Ui


class AiDataScraper(abc.ABC):
    @abc.abstractmethod
    def __call__(self, ui: Ui, ai: AiReader):
        pass

    @property
    @abc.abstractmethod
    def answer(self):
        pass

