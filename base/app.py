import os
import signal
import subprocess
import time

import pygetwindow

from base.ui import Ui


class App:
    def __init__(self, path_to_exe: str, window_title_name: str | None = None):
        self.__process: subprocess.Popen | None = None
        self.__path = path_to_exe
        all_windows = pygetwindow.getAllWindows()
        self.start_app()
        if not window_title_name:
            window = [i for i in pygetwindow.getAllWindows() if i not in all_windows][0]
        else:
            window = pygetwindow.getWindowsWithTitle(window_title_name)
        self.__ui = Ui(window)

    def start_app(self):
        self.__process = subprocess.Popen([self.__path])
        time.sleep(2)

    def stop_app(self):
        self.__process.kill()
        self.ui.close_window()

    @property
    def ui(self):
        return self.__ui
