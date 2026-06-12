import importlib
import numpy

from apparser.text_readers.readers.base import BaseTextReader
from apparser.text_readers.models.text_data import TextData

from apparser.geometry import Point, QuadPoints


class EasyOcrReader(BaseTextReader):
    """Read text from images by using EasyOCR."""

    def __init__(self, lang_list: list[str] = None, **settings):
        """Initialize an EasyOCR-backed text reader.

        :param lang_list: Languages passed to the EasyOCR reader.
        :type lang_list: list[str] | None
        :param settings: Additional EasyOCR reader settings.
        :type settings: dict[str, object]
        """
        if lang_list is None:
            lang_list = ["en"]
        easyocr = importlib.import_module("easyocr")
        self.__reader = easyocr.Reader(lang_list, **settings)

    def read_image(self, image: numpy.ndarray, **settings) -> list[TextData]:
        """Read text data from an image.

        :param image: Image data to process.
        :type image: numpy.ndarray
        :param settings: Additional EasyOCR read settings.
        :type settings: dict[str, object]
        :return: Detected text data.
        :rtype: list[TextData]
        """
        returned = []
        predicted = self.__reader.readtext(image, **settings)
        for i in predicted:
            points = QuadPoints(*[Point(int(j[0]), int(j[1])) for j in i[0]])
            text_data = TextData(i[1], points)
            returned.append(text_data)
        return returned
