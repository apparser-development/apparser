import abc

import numpy


class BaseSpeaker(abc.ABC):
    """Define the common interface for speech synthesis backends."""

    @abc.abstractmethod
    def speak(self, text: str) -> tuple[numpy.ndarray, int]:
        """Convert text into audio data.

        :param text: Text to synthesize.
        :type text: str
        :return: Generated audio samples and bitrate.
        :rtype: tuple[numpy.ndarray, int]
        """
        pass
