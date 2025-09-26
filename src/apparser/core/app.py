import subprocess
import time

from appwindows import get_finder

from apparser.core.ui import Ui
from apparser.geometry import Size


class App:
    def __init__(self, path_to_exe: str,
                 window_title: str,
                 window_size: Size = Size(900, 900),
                 timeout: float = 1):
        self.__window_finder = get_finder()
        self.__process: subprocess.Popen | None = None
        self.__path = path_to_exe
        self.__timeout = timeout
        self.__window_size: Size = window_size
        self.__window_title_name: str = window_title
        self.__ui: Ui | None = None
        self.start_app()

    def start_app(self):
        self.__process = subprocess.Popen([self.__path])
        time.sleep(self.__timeout)
        window = self.__window_finder.get_window_by_title(self.__window_title_name)
        self.__ui = Ui(window)
        self.__ui.window.resize(self.__window_size)

    def stop_app(self):
        self.ui.window.close()
        self.__process.kill()

    @property
    def ui(self) -> Ui:
        return self.__ui
