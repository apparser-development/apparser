import abc
import numpy


class AiReader(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def read_image(self, image: numpy.ndarray) -> list:
        pass