import abc

import numpy

from apparser.text_readers.models.text_data import TextData


class BaseTextReader(abc.ABC):
    """Define the common interface for text reader backends."""

    @abc.abstractmethod
    def read_image(self, image: numpy.ndarray) -> list[TextData]:
        """Read text data from an image.

        :param image: Image data to process.
        :type image: numpy.ndarray
        :return: Detected text data.
        :rtype: list[TextData]
        """
        pass
