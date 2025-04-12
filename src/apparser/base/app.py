import subprocess
import time

import pygetwindow

from apparser.base.ui import Ui
from apparser.base.window import Window


class App:
    def __init__(self, path_to_exe: str,
                 window_size: tuple[int, int] = (900, 900),
                 window_title_name: str | None = None,
                 timeout: float = 0.1):
        self.__process: subprocess.Popen | None = None
        self.__path = path_to_exe
        self.__timeout = timeout
        self.__window_size: tuple[int, int] = window_size
        self.__window_title_name: str = window_title_name
        self.__ui: Ui | None = None
        self.start_app()

    def start_app(self):
        all_windows = pygetwindow.getAllWindows()
        self.__process = subprocess.Popen([self.__path])
        time.sleep(self.__timeout)
        if not self.__window_title_name:
            window = [i for i in pygetwindow.getAllWindows() if i not in all_windows][0]
        else:
            window = pygetwindow.getWindowsWithTitle(self.__window_title_name)[0]
        window = Window(window)
        self.__ui = Ui(window)
        self.__ui.window.size = self.__window_size

    def stop_app(self):
        self.ui.window.close()
        self.__process.kill()

    @property
    def ui(self) -> Ui:
        return self.__ui
