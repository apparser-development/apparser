import abc
from typing import Type

from apparser.core import Ui
from apparser.cv.events import CvEvent
from apparser.cv.models import CvAllData, CvClassData


class CvHandlers(abc.ABC):
    @abc.abstractmethod
    def register_handler(self, event: Type[CvEvent]):
        pass

    @abc.abstractmethod
    def call(self, event: Type[CvEvent], all_data: CvAllData, ui: Ui, class_data: CvClassData):
        pass
