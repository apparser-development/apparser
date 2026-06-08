import importlib
from typing import Any

import numpy
from appwindows.geometry import QuadPoints

from apparser.geometry import Point
from apparser.text_readers.detectors.base import BaseTextDetector


def _build_box_points(
    left: int,
    top: int,
    right: int,
    bottom: int,
) -> QuadPoints:
    return QuadPoints(
        Point(left, top),
        Point(right, top),
        Point(right, bottom),
        Point(left, bottom),
    )


def _parse_horizontal_box(box: Any) -> QuadPoints | None:
    array = numpy.asarray(box)
    if array.ndim != 1 or array.size < 4:
        return None
    left, right, top, bottom = array[:4]
    return _build_box_points(
        int(left),
        int(top),
        int(right),
        int(bottom),
    )


def _parse_free_box(box: Any) -> QuadPoints | None:
    array = numpy.asarray(box)
    if array.ndim == 1 and array.size >= 8 and array.size % 2 == 0:
        array = array.reshape(-1, 2)
    if array.ndim != 2 or len(array) < 4 or array.shape[-1] < 2:
        return None
    points = [
        Point(int(coordinates[0]), int(coordinates[1]))
        for coordinates in array[:4]
    ]
    return QuadPoints(*points)


def _extend_horizontal_points(
    returned: list[QuadPoints],
    horizontal_groups: Any,
) -> None:
    for group in horizontal_groups:
        points = _parse_horizontal_box(group)
        if points is not None:
            returned.append(points)
            continue

        for box in group:
            points = _parse_horizontal_box(box)
            if points is not None:
                returned.append(points)


def _extend_free_points(
    returned: list[QuadPoints],
    free_groups: Any,
) -> None:
    for group in free_groups:
        points = _parse_free_box(group)
        if points is not None:
            returned.append(points)
            continue

        for box in group:
            points = _parse_free_box(box)
            if points is not None:
                returned.append(points)


def _parse_detect_result(predicted: Any) -> list[QuadPoints]:
    returned: list[QuadPoints] = []

    if len(predicted) < 2:
        return returned

    horizontal_groups, free_groups = predicted[:2]
    _extend_horizontal_points(returned, horizontal_groups)
    _extend_free_points(returned, free_groups)
    return returned


def _build_default_settings(settings: dict[str, Any]) -> dict[str, Any]:
    default_settings: dict[str, Any] = {
        "detector": True,
        "recognizer": False,
    }
    default_settings.update(settings)
    return default_settings


class EasyOcrDetector(BaseTextDetector):
    def __init__(
        self,
        lang_list: list[str] | None = None,
        **settings: Any,
    ) -> None:
        if lang_list is None:
            lang_list = ["en"]
        easyocr = importlib.import_module("easyocr")
        self.__reader = easyocr.Reader(
            lang_list,
            **_build_default_settings(settings),
        )

    def read_image(
        self,
        image: numpy.ndarray,
        **settings: Any,
    ) -> list[QuadPoints]:
        predicted = self.__reader.detect(image, **settings)
        return _parse_detect_result(predicted)
