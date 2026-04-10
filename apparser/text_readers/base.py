import abc

import numpy

from apparser.text_readers.models.text_data import TextData


class BaseTextReader(abc.ABC):
    @abc.abstractmethod
    def read_image(self, image: numpy.ndarray) -> list[TextData]:
        pass
