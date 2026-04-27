import numpy

from apparser.text_readers.base import BaseTextReader
from apparser.text_readers.models.text_data import TextData

from PIL import Image


class WhiteBlackReader(BaseTextReader):
    """Convert images to grayscale before OCR processing."""

    def __init__(self, reader: BaseTextReader):
        """Initialize a grayscale text reader wrapper.

        :param reader: Reader used after grayscale conversion.
        :type reader: BaseTextReader
        """
        self.__reader = reader

    def read_image(self, image: numpy.ndarray) -> list[TextData]:
        """Read text data from a grayscale version of the image.

        :param image: Image data to process.
        :type image: numpy.ndarray
        :return: Detected text data.
        :rtype: list[TextData]
        """
        image = Image.fromarray(image)
        image = image.convert('L')
        return self.__reader.read_image(numpy.array(image))
