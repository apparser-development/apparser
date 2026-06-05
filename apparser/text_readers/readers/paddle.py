import importlib
from typing import Any
import numpy
from appwindows.geometry import QuadPoints

from apparser.geometry import Point
from apparser.text_readers.readers.base import BaseTextReader
from apparser.text_readers.models.text_data import TextData


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


def _parse_points_geometry(geometry: Any) -> QuadPoints | None:
    array = numpy.asarray(geometry)

    if array.ndim == 1 and array.size == 4:
        left, top, right, bottom = array[:4]
        return _build_box_points(
            int(left),
            int(top),
            int(right),
            int(bottom),
        )

    if array.ndim == 1 and array.size >= 8 and array.size % 2 == 0:
        array = array.reshape(-1, 2)

    if array.ndim >= 2 and array.shape[-1] >= 2:
        x_coordinates = array[..., 0].reshape(-1)
        y_coordinates = array[..., 1].reshape(-1)

        if len(x_coordinates) == 0 or len(y_coordinates) == 0:
            return None

        return _build_box_points(
            int(x_coordinates.min()),
            int(y_coordinates.min()),
            int(x_coordinates.max()),
            int(y_coordinates.max()),
        )

    return None


def _parse_predict_result(predicted: list[Any]) -> list[TextData]:
    returned: list[TextData] = []

    for item in predicted:
        if hasattr(item, "res"):
            item = item.res

        if not isinstance(item, dict):
            continue

        texts = item.get("rec_texts")
        polygons = item.get("rec_polys")

        if polygons is None:
            polygons = item.get("dt_polys")

        boxes = item.get("rec_boxes")
        geometries = polygons if polygons is not None else boxes

        if texts is None or geometries is None:
            continue

        for index in range(min(len(texts), len(geometries))):
            points = _parse_points_geometry(geometries[index])
            if points is None:
                continue
            returned.append(TextData(texts[index], points))

    return returned


def _build_default_settings(
        settings: dict[str, Any],
    enable_mkldnn: bool,
) -> dict[str, Any]:
    default_settings = {
        "enable_mkldnn": enable_mkldnn,
        "use_doc_orientation_classify": False,
        "use_doc_unwarping": False,
        "use_textline_orientation": False,
    }
    default_settings.update(settings)
    return default_settings


class PaddleTextReader(BaseTextReader):
    def __init__(
        self,
        lang: str = "en",
        enable_mkldnn: bool = False,
        **settings: Any,
    ) -> None:
        self.__lang = lang
        self.__enable_mkldnn = enable_mkldnn
        self.__settings = _build_default_settings(
            settings,
            enable_mkldnn,
        )
        self.__reader = self.__create_reader(self.__settings)

    def read_image(
        self,
        image: numpy.ndarray,
        **settings: Any,
    ) -> list[TextData]:
        predicted = self.__reader.predict(image, **settings)
        return _parse_predict_result(predicted)

    def __create_reader(self, settings: dict[str, Any]) -> Any:
        paddleocr = importlib.import_module("paddleocr")
        return paddleocr.PaddleOCR(lang=self.__lang, **settings)
