import abc

from apparser.cv.events import CvEvent


class CvHandler(abc.ABC):
    @abc.abstractmethod
    @property
    def register(event: CvEvent):
        pass