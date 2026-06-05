import numpy

from apparser.text_readers.readers.base import BaseTextReader
from apparser.text_readers.models import TextData

from apparser.text_readers.detectors import BaseTextDetector
from apparser.text_readers.scanners import BaseTextScanner


class CompoundReader(BaseTextReader):
    """Convert images to grayscale before OCR processing."""

    def __init__(self, detector: BaseTextDetector, scanner: BaseTextScanner ):
        """Initialize a grayscale text reader wrapper.

        :param detector: Detector to detect text in image
        :type detector: BaseTextDetector
        :param scanner: Scanner to read text from image
        :type scanner: BaseTextScanner
        :raises TypeError: If any argument has an invalid type.
        """
        if not isinstance(detector, BaseTextDetector):
            raise TypeError('detector must be an instance of BaseTextDetector')

        if not isinstance(scanner, BaseTextScanner):
            raise TypeError('scanner must be an instance of BaseTextScanner')

        self.__scanner = scanner
        self.__detector = detector

    def read_image(self, image: numpy.ndarray) -> list[TextData]:
        """Read text data.

        :param image: Image data to process.
        :type image: numpy.ndarray
        :return: Detected text data.
        :rtype: list[TextData]
        """
        pass
