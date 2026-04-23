import abc

import numpy


class BaseSpeaker(abc.ABC):
    @abc.abstractmethod
    def speak(self, text: str) -> numpy.ndarray:
        pass