import importlib

import numpy

from apparser.text_readers.base import BaseTextReader
from apparser.text_readers.models.text_data import TextData

from apparser.geometry import Point


def _parse_predict_result(predicted) -> list[TextData]:
    returned = []
    for i in predicted:
        if hasattr(i, "res"):
            i = i.res
        if not isinstance(i, dict):
            continue
        texts = i.get("rec_texts")
        polygons = i.get("rec_polys")
        if polygons is None:
            polygons = i.get("dt_polys")
        if texts is None or polygons is None:
            continue
        for j in range(min(len(texts), len(polygons))):
            points = [Point(int(k[0]), int(k[1])) for k in polygons[j]]
            text_data = TextData(texts[j], points)
            returned.append(text_data)
    return returned


def _is_ocr_line(data: object) -> bool:
    return (isinstance(data, (list, tuple))
            and len(data) >= 2
            and isinstance(data[0], (list, tuple, numpy.ndarray))
            and isinstance(data[1], (list, tuple))
            and len(data[1]) >= 1)


def _parse_ocr_result(predicted) -> list[TextData]:
    returned = []
    if (len(predicted) == 1
            and isinstance(predicted[0], list)
            and len(predicted[0]) > 0
            and _is_ocr_line(predicted[0][0])):
        predicted = predicted[0]
    for i in predicted:
        if i is None or not _is_ocr_line(i):
            continue
        points = [Point(int(j[0]), int(j[1])) for j in i[0]]
        text_data = TextData(i[1][0], points)
        returned.append(text_data)
    return returned


class PaddleTextReader(BaseTextReader):
    def __init__(self, lang: str = "en", **settings):
        paddleocr = importlib.import_module("paddleocr")
        self.__reader = paddleocr.PaddleOCR(lang=lang, **settings)

    def read_image(self, image: numpy.ndarray, **settings) -> list[TextData]:
        if hasattr(self.__reader, "predict"):
            predicted = self.__reader.predict(image, **settings)
            return _parse_predict_result(predicted)
        predicted = self.__reader.ocr(image, **settings)
        return _parse_ocr_result(predicted)
