import abc

from apparser.core import BaseUi
from apparser.cv.handlers import CvHandlers


class CvProcess(abc.ABC):
    @abc.abstractmethod
    def start(self, ui: BaseUi):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def include_handlers(self, handler: CvHandlers):
        pass