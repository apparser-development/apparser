import subprocess
import time

from appwindows import get_finder
from appwindows.exceptions import WindowDoesNotFoundException, WindowDoesNotValidException

from apparser.core.ui import WindowUi, BaseUi


class App:
    """Manage an application process and its UI wrapper."""

    def __init__(self, start_command: str | list[str],
                 window_title: str | None = None,
                 timeout: float = 1):
        """Initialize an application controller.

        :param start_command: App start command.
        :type start_command: str
        :param window_title: Title of the window to attach to.
        :type window_title: str
        :param timeout: Delay before the window lookup starts.
        :type timeout: float
        :raises TypeError: If any argument has an invalid type.
        """
        if isinstance(start_command, str):
            start_command = [start_command]

        if not isinstance(start_command, list):
            raise TypeError('start_command must be a string or list[str]')

        if window_title is not None and not isinstance(window_title, str):
            raise TypeError('window_title must be a string')

        if not (isinstance(timeout, float) or isinstance(timeout, int)):
            raise TypeError('timeout must be a number')

        self.__window_finder = get_finder()
        self.__process: subprocess.Popen | None = None
        self.__start_command = start_command
        self.__timeout = timeout
        self.__window_title_name: str = window_title
        self.__ui: BaseUi | None = None
        self.start_app()

    def __find_window_by_title(self):
        try:
            window = self.__window_finder.get_window_by_title(self.__window_title_name)
            self.__ui = WindowUi(window)
        except WindowDoesNotFoundException:
            pass

    def __find_window_by_process_id(self, process_id: int):
        try:
            window = self.__window_finder.get_window_by_process_id(process_id)
            self.__ui = WindowUi(window)
        except WindowDoesNotFoundException:
            pass

    def start_app(self):
        """Start the application process and bind its UI.

        :raises WindowDoesNotValidException: If the window is not found or the application cannot be opened.
        """
        if self.__window_title_name is not None:
            self.__find_window_by_title()
        if self.__ui is not None:
            return
        window_processes = [i.get_process_id() for i in get_finder().get_all_windows()]
        self.__process = subprocess.Popen(self.__start_command)
        time.sleep(self.__timeout)
        self.__find_window_by_process_id(self.__process.pid)
        for i in get_finder().get_all_windows():
            if self.__ui is not None:
                return
            if i.get_process_id() not in window_processes:
                self.__find_window_by_process_id(i.get_process_id())
        if self.__ui is not None:
            return
        self.__find_window_by_title()
        if self.__ui is None:
            raise WindowDoesNotValidException()

    def stop_app(self):
        """Close the application window and stop the process."""
        self.ui.window.close()
        if self.__process is not None:
            self.__process.kill()

    @property
    def ui(self) -> BaseUi:
        """Return the UI wrapper for the running application.

        :return: UI wrapper bound to the application window.
        :rtype: BaseUi
        """
        return self.__ui
