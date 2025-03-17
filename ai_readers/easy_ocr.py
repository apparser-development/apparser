import easyocr
import numpy

from ai_readers.base import AiReader
from ai_readers.text_data import TextData
from base import Point


class EasyOcrReader(AiReader):
    def __init__(self):
        super().__init__()
        self.__reader = easyocr.Reader(['en'])

    def read_image(self, image: numpy.ndarray) -> list[TextData]:
        returned = []
        predicted = self.__reader.readtext(image)
        for i in predicted:
            points = [Point(int(j[0]), int(j[1])) for j in i[0]]
            text_data = TextData(i[1], points)
            returned.append(text_data)
        return returned
