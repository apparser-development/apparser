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
        all_windows = pygetwindow.getAllWindows()
        self.start_app()
        time.sleep(timeout)
        if not window_title_name:
            window = [i for i in pygetwindow.getAllWindows() if i not in all_windows][0]
        else:
            window = pygetwindow.getWindowsWithTitle(window_title_name)[0]
        window = Window(window)
        self.__ui = Ui(window)
        self.__ui.window.size = window_size

    def start_app(self):
        self.__process = subprocess.Popen([self.__path])
        time.sleep(2)

    def stop_app(self):
        self.ui.window.close()
        self.__process.kill()

    @property
    def ui(self) -> Ui:
        return self.__ui
