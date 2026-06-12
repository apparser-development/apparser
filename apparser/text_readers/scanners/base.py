import abc

import numpy


class BaseTextScanner(abc.ABC):
    """Define the common interface for text scanner backends."""

    @abc.abstractmethod
    def read_image(self, image: numpy.ndarray) -> str:
        """Read text from an image.

        :param image: Image data to process.
        :type image: numpy.ndarray
        :return: Detected text.
        :rtype: str
        """
        pass
