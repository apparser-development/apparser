import abc

from apparser.cv.events import CvEvent
from apparser.cv.models import CvData


class CvHandler(abc.ABC):
    @abc.abstractmethod
    def register_event(self, event: CvEvent):
        pass

    @abc.abstractmethod
    def call(self, event: CvEvent, data: CvData):
        pass