import abc
from typing import Type

from apparser.cv.events import CvEvent
from apparser.cv.models import CvChangeData


class CvHandlers(abc.ABC):
    @abc.abstractmethod
    def register_handler(self, event: Type[CvEvent]):
        pass

    @abc.abstractmethod
    def call(self, event: Type[CvEvent], changed_data: CvChangeData, *args):
        pass
