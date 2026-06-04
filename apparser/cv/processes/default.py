import time

from apparser.core import BaseUi

from apparser.cv.handlers import CvHandlers
from apparser.cv.processes.base import CvProcess
from apparser.cv.readers import CvReader
from apparser.cv.utils import ChangesChecker


class DefaultCvProcess(CvProcess):
    """Run a reader, detect changes, and dispatch matching handlers."""

    def __init__(
        self,
        reader: CvReader,
        sleep_seconds: float = 3,
        changes_checker: ChangesChecker = None,
    ):
        """Initialize the default computer vision process.

        :param reader: Reader used to collect computer vision data.
        :type reader: CvReader
        :param sleep_seconds: Delay between read cycles in seconds.
        :type sleep_seconds: float
        :param changes_checker: Change detector used between read cycles.
        :type changes_checker: ChangesChecker | None
        """
        if changes_checker is None:
            changes_checker = ChangesChecker()

        self.__sleep_seconds = sleep_seconds
        self.__is_working = True
        self.__reader = reader
        self.__handlers_list: list[CvHandlers] = []
        self.__checker = changes_checker

    def start(self, ui: BaseUi):
        """Start reading frames and dispatching detected changes.

        :param ui: UI instance used as the screenshot source.
        :type ui: BaseUi
        """
        self.__is_working = True
        while self.__is_working:
            cv_data = self.__reader.read(ui)
            for class_data in self.__checker.check(cv_data):
                for handler in self.__handlers_list:
                    handler.call(class_data.event, class_data, cv_data, ui)

            if self.__is_working and self.__sleep_seconds > 0:
                time.sleep(self.__sleep_seconds)

    def stop(self):
        """Request the processing loop to stop."""
        self.__is_working = False

    def include_handlers(self, handler: CvHandlers):
        """Attach a handler registry to the process.

        :param handler: Handler registry to append.
        :type handler: CvHandlers
        """
        self.__handlers_list.append(handler)
