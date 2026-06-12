from apparser.geometry import QuadPoints, distance, Point

from apparser.text_readers.readers.base import BaseTextReader

from apparser.text_readers.models import TextData
from apparser.text_readers.detectors import BaseTextDetector
from apparser.text_readers.scanners import BaseTextScanner


import numpy
from PIL import Image


def _cut_by_coordinates(image: numpy.ndarray, coordinates: QuadPoints) -> numpy.ndarray:
    pil_image = Image.fromarray(image)
    if pil_image.mode not in ("RGB", "RGBA", "L"):
        pil_image = pil_image.convert("RGB")
    left_top = Point(coordinates.left_top.x, coordinates.left_top.y)
    right_top = Point(coordinates.right_top.x, coordinates.right_top.y)
    right_bottom = Point(coordinates.right_bottom.x, coordinates.right_bottom.y)
    left_bottom = Point(coordinates.left_bottom.x, coordinates.left_bottom.y)
    out_width = int(max(distance(left_top, right_top), distance(left_bottom, right_bottom)))
    out_height = int(max(distance(left_top, left_bottom), distance(right_top, right_bottom)))
    out_size = (max(out_width, 1), max(out_height, 1))
    quad_data = (left_top.x, left_top.y,
                 right_top.x, right_top.y,
                 right_bottom.x, right_bottom.y,
                 left_bottom.x, left_bottom.y)
    transformed = pil_image.transform(out_size, Image.QUAD, quad_data,
                                      resample=Image.BICUBIC)
    return numpy.array(transformed)


class CompoundReader(BaseTextReader):
    """Detect text regions and scan each detected image fragment."""

    def __init__(self, detector: BaseTextDetector, scanner: BaseTextScanner ):
        """Initialize a compound text reader.

        :param detector: Detector used to find text regions in an image.
        :type detector: BaseTextDetector
        :param scanner: Scanner used to read text from detected image fragments.
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
        result = []
        for coordinates in self.__detector.read_image(image):
            cuted_image = _cut_by_coordinates(image, coordinates)
            text = self.__scanner.read_image(cuted_image)
            result.append(TextData(text=text, coordinates=coordinates))
        return result
