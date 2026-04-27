import subprocess
import time

from appwindows import get_finder

from apparser.core.ui.window import WindowUi, BaseUi
from apparser.geometry import Size


class App:
    """Manage an application process and its UI wrapper."""

    def __init__(self, path_to_exe: str,
                 window_title: str,
                 window_size: Size = Size(900, 900),
                 timeout: float = 1):
        """Initialize an application controller.

        :param path_to_exe: Path to the executable file.
        :type path_to_exe: str
        :param window_title: Title of the window to attach to.
        :type window_title: str
        :param window_size: Initial size applied to the window.
        :type window_size: Size
        :param timeout: Delay before the window lookup starts.
        :type timeout: float
        :raises TypeError: If any argument has an invalid type.
        """
        if not isinstance(path_to_exe, str):
            raise TypeError('path_to_exe must be a string')

        if not isinstance(window_title, str):
            raise TypeError('window_title must be a string')

        if not isinstance(window_size, Size):
            raise TypeError('window_size must be a Size')

        if not (isinstance(timeout, float) or isinstance(timeout, int)):
            raise TypeError('timeout must be a number')

        self.__window_finder = get_finder()
        self.__process: subprocess.Popen | None = None
        self.__path = path_to_exe
        self.__timeout = timeout
        self.__window_size: Size = window_size
        self.__window_title_name: str = window_title
        self.__ui: BaseUi | None = None
        self.start_app()

    def start_app(self):
        """Start the application process and bind its UI."""
        self.__process = subprocess.Popen([self.__path])
        time.sleep(self.__timeout)
        window = self.__window_finder.get_window_by_title(self.__window_title_name)
        self.__ui = WindowUi(window)
        self.__ui.window.resize(self.__window_size)

    def stop_app(self):
        """Close the application window and stop the process."""
        self.ui.window.close()
        self.__process.kill()

    @property
    def ui(self) -> BaseUi:
        """Return the UI wrapper for the running application.

        :return: UI wrapper bound to the application window.
        :rtype: BaseUi
        """
        return self.__ui
