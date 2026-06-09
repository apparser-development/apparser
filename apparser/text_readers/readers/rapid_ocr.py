import importlib
from typing import Any

import numpy

from apparser.geometry import Point, QuadPoints
from apparser.text_readers.models import TextData
from apparser.text_readers.readers.base import BaseTextReader


def _build_box_points(geometry: Any) -> QuadPoints | None:
    array = numpy.asarray(geometry)
    if array.ndim == 1 and array.size == 4:
        left, top, right, bottom = array[:4]
        return QuadPoints(
            Point(int(left), int(top)),
            Point(int(right), int(top)),
            Point(int(right), int(bottom)),
            Point(int(left), int(bottom)),
        )
    if array.ndim == 1 and array.size >= 8 and array.size % 2 == 0:
        array = array.reshape(-1, 2)
    if array.ndim != 2 or len(array) < 4 or array.shape[-1] < 2:
        return None
    return QuadPoints(
        *[Point(int(coordinates[0]), int(coordinates[1]))
          for coordinates in array[:4]]
    )


def _parse_output_object(predicted: Any) -> list[TextData] | None:
    if not hasattr(predicted, "boxes") and not hasattr(predicted, "txts"):
        return None
    boxes = getattr(predicted, "boxes", None)
    texts = getattr(predicted, "txts", None)
    if boxes is None or texts is None:
        return []
    return _parse_boxes_and_texts(boxes, texts)


def _parse_result_item(item: Any) -> TextData | None:
    if not isinstance(item, (list, tuple)) or len(item) < 2:
        return None
    points = _build_box_points(item[0])
    if points is None:
        return None
    return TextData(str(item[1]), points)


def _parse_result_list(predicted: Any) -> list[TextData]:
    if predicted is None:
        return []
    returned: list[TextData] = []
    try:
        iterator = iter(predicted)
    except TypeError:
        return []
    for item in iterator:
        text_data = _parse_result_item(item)
        if text_data is not None:
            returned.append(text_data)
    return returned


def _parse_boxes_and_texts(boxes: Any, texts: Any) -> list[TextData]:
    returned: list[TextData] = []
    for box, text in zip(boxes, texts):
        points = _build_box_points(box)
        if points is not None:
            returned.append(TextData(str(text), points))
    return returned


def _parse_predict_result(predicted: Any) -> list[TextData]:
    parsed = _parse_output_object(predicted)
    if parsed is not None:
        return parsed
    if isinstance(predicted, tuple) and len(predicted) == 2:
        predicted = predicted[0]
    return _parse_result_list(predicted)


class RapidOcrReader(BaseTextReader):
    """Read text from images by using RapidOCR."""

    def __init__(self, **settings: Any) -> None:
        """Initialize a RapidOCR-backed text reader.

        :param settings: Additional RapidOCR reader settings.
        :type settings: dict[str, object]
        """
        rapidocr = importlib.import_module("rapidocr")
        self.__reader = rapidocr.RapidOCR(**settings)

    def read_image(
            self,
            image: numpy.ndarray,
            **settings: Any,
    ) -> list[TextData]:
        """Read text data from an image.

        :param image: Image data to process.
        :type image: numpy.ndarray
        :param settings: Additional RapidOCR read settings.
        :type settings: dict[str, object]
        :return: Detected text data.
        :rtype: list[TextData]
        """
        predicted = self.__reader(image, **settings)
        return _parse_predict_result(predicted)
