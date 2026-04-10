import numpy

from apparser.text_readers.base import BaseTextReader
from apparser.text_readers.models.text_data import TextData


class ScreensController(BaseTextReader):
    def __init__(self, ai_reader: BaseTextReader):
        self.__screens: list[numpy.ndarray] = []
        self.__texts: list[list[TextData]] = []
        self.__ai_reader = ai_reader

    def __find_every_checked_screen(self, image: numpy.ndarray) -> int:
        for i in range(len(self.__screens)):
            if numpy.array_equal(image, self.__screens[i]):
                return i
        return -1

    def read_image(self, image: numpy.ndarray) -> list[TextData]:
        screen_id = self.__find_every_checked_screen(image)
        if screen_id != -1:
            return self.__texts[screen_id]
        texts = self.__ai_reader.read_image(image)
        self.__texts.append(texts)
        self.__screens.append(image)
        return texts
