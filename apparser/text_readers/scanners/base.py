import abc

import numpy

from apparser.text_readers.models.text_data import TextData


class BaseTextScanner(abc.ABC):
    """Define the common interface for text reader backends."""

    @abc.abstractmethod
    def read_image(self, image: numpy.ndarray) -> str:
        """Read text data from an image.

        :param image: Image data to process.
        :type image: numpy.ndarray
        :return: Detected text data.
        :rtype: list[TextData]
        """
        pass
