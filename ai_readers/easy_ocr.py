import easyocr
import numpy

from ai_readers.base import AiReader


class EasyOcrReader(AiReader):
    def __init__(self):
        super().__init__()
        self.__reader = easyocr.Reader(['en'])

    def read_image(self, image: numpy.ndarray) -> list:
        return self.__reader.readtext(image)
