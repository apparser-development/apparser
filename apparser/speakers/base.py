import abc

import numpy


class Speaker(abc.ABC):
    @abc.abstractmethod
    def speak(self, text: str) -> numpy.ndarray:
        pass