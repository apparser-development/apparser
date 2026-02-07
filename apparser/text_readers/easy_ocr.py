import easyocr
import numpy

from apparser.text_readers.base import AiReader
from apparser.text_readers.text_data import TextData

from apparser.core.geometry import Point


class EasyOcrReader(AiReader):
    def __init__(self, lang_list: list[str] = None, **settings):
        if lang_list is None:
            lang_list = ["en"]
        self.__reader = easyocr.Reader(lang_list, **settings)

    def read_image(self, image: numpy.ndarray, **settings) -> list[TextData]:
        returned = []
        predicted = self.__reader.readtext(image, **settings)
        for i in predicted:
            points = [Point(int(j[0]), int(j[1])) for j in i[0]]
            text_data = TextData(i[1], points)
            returned.append(text_data)
        return returned
