import numpy

from apparser.ai_readers.base import AiReader


class PaddleOcrReader(AiReader):
    def __init__(self):
        pass

    def read_image(self, image: numpy.ndarray) -> list:
        pass