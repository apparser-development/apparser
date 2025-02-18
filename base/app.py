from base.ui import Ui


class App:
    def __init__(self, path_to_exe: str):
        self.__path = path_to_exe
        self.start_app()
        self.__ui = Ui()

    def start_app(self):
        pass

    def stop_app(self):
        pass

    @property
    def ui(self):
        return self.__ui


