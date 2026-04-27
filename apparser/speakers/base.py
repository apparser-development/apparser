import abc

import numpy


class BaseSpeaker(abc.ABC):
    """Define the common interface for speech synthesis backends."""

    @abc.abstractmethod
    def speak(self, text: str) -> numpy.ndarray:
        """Convert text into audio data.

        :param text: Text to synthesize.
        :type text: str
        :return: Generated audio samples.
        :rtype: numpy.ndarray
        """
        pass
