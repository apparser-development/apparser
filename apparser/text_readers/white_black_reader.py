import numpy

from apparser.text_readers.base import BaseTextReader
from apparser.text_readers.models.text_data import TextData

from PIL import Image


class WhiteBlackReader(BaseTextReader):
    def __init__(self, reader: BaseTextReader):
        self.__reader = reader

    def read_image(self, image: numpy.ndarray) -> list[TextData]:
        image = Image.fromarray(image)
        image = image.convert('L')
        return self.__reader.read_image(numpy.array(image))
