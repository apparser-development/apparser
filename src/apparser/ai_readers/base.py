import abc

import numpy

from apparser.ai_readers.text_data import TextData


class AiReader(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def read_image(self, image: numpy.ndarray) -> list[TextData]:
        pass
