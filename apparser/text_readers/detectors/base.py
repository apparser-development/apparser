import abc

import numpy

from apparser.geometry import QuadPoints


class BaseTextDetector(abc.ABC):
    """Define the common interface for text detection backends."""

    @abc.abstractmethod
    def read_image(self, image: numpy.ndarray) -> list[QuadPoints]:
        """Detect text coordinates in an image.

        :param image: Image data to process.
        :type image: numpy.ndarray
        :return: Detected text coordinates.
        :rtype: list[QuadPoints]
        """
        pass
