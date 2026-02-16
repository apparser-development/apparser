import abc

from apparser.cv.handlers import CvHandler


class CvProcess(abc.ABC):
    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def add_handler(self, handler: CvHandler):
        pass