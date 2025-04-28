import numpy

from apparser.ai_readers.base import AiReader
from apparser.ai_readers.text_data import TextData

from PIL import Image


class WhiteBlackReader(AiReader):
    def __init__(self, reader: AiReader):
        self.__reader = reader

    def read_image(self, image: numpy.ndarray) -> list[TextData]:
        image = Image.fromarray(image)
        image = image.convert('L')
        return self.__reader.read_image(numpy.array(image))
