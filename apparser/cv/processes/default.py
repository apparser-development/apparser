from apparser.core import Ui

from apparser.cv.handlers import CvHandlers
from apparser.cv.processes.base import CvProcess
from apparser.cv.readers import CvReader, YoloReader
from apparser.cv.utils import ChangesChecker


class DefaultCvProcess(CvProcess):
    def __init__(self, reader: CvReader = YoloReader(), sleep_seconds: float = 3,
                 changes_checker: ChangesChecker = ChangesChecker()):
        self.__sleep_seconds = sleep_seconds
        self.__is_working = True
        self.__reader = reader
        self.__handlers_list: list[CvHandlers] = []
        self.__checker = changes_checker

    def start(self, ui: Ui):
        self.__is_working = True
        while self.__is_working:
            image = ui.window.get_screenshot()
            cv_data = self.__reader.read(image)
            for class_data in self.__checker.check(cv_data):
                for handler in self.__handlers_list:
                    handler.call(class_data.event, class_data, cv_data, self.__ui)

    def stop(self):
        self.__is_working = False

    def include_handlers(self, handler: CvHandlers):
        self.__handlers_list.append(handler)
