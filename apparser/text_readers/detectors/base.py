import abc

import numpy

from apparser.geometry import QuadPoints


class BaseTextDetector(abc.ABC):
    """Define the common interface for text reader backends."""

    @abc.abstractmethod
    def read_image(self, image: numpy.ndarray) -> list[QuadPoints]:
        """Read text data from an image.

        :param image: Image data to process.
        :type image: numpy.ndarray
        :return: Detected text data.
        :rtype: list[TextData]
        """
        pass
