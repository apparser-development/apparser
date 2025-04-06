import abc

import numpy

from apparser.ai_readers.text_data import TextData

class AiReader(abc.ABC):
    @abc.abstractmethod
    def read_image(self, image: numpy.ndarray) -> list[TextData]:
        pass
