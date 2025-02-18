import numpy

from ai_readers.base import AiReader


class PaddleOcrReader(AiReader):
    def __init__(self):
        super().__init__()

    def read_image(self, image: numpy.ndarray) -> list:
        pass