"""YOLO-based computer vision reader implementation."""

from __future__ import annotations

from apparser.geometry import Point, Size
from ultralytics import YOLO

from apparser import CoordinatesUi
from apparser.core import BaseUi
from apparser.cv.models import CvAllData, CvBox
from apparser.cv.readers.base import CvReader


class YoloReader(CvReader):
    """Read detected objects from UI screenshots with YOLO tracking."""

    def __init__(self, model: object | str, persist: bool = True, **track_settings):
        """Initialize a YOLO reader.

        :param model: YOLO model instance or path used to create one.
        :type model: object | str
        :param persist: Whether to preserve tracking identifiers between reads.
        :type persist: bool
        :param track_settings: Additional keyword arguments forwarded to ``track``.
        """
        if hasattr(model, "track"):
            self.__model = model
        else:
            self.__model = YOLO(model=model)

        self.__persist = persist
        self.__track_settings = track_settings

    def read(self, ui: BaseUi) -> CvAllData:
        """Read object detections from the provided UI screenshot.

        :param ui: UI instance used as the screenshot source.
        :type ui: BaseUi
        :return: Detected boxes with their local UI wrappers.
        :rtype: CvAllData
        """
        results = self.__model.track(
            source=ui.get_screenshot(),
            persist=self.__persist,
            **self.__track_settings,
        )[0]
        boxes = []
        names = self.__model.model.names
        for box in results.boxes:
            track_id = box.id
            class_index = int(box.cls.item())
            if track_id is not None:
                track_id = int(track_id.item())
            cls_name = names[class_index]
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            x = int(x1)
            y = int(y1)
            width = int(x2 - x1)
            height = int(y2 - y1)
            box_ui = CoordinatesUi(ui, Point(x, y), Size(width, height))
            boxes.append(
                CvBox(
                    class_name=cls_name,
                    track_id=track_id,
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    ui=box_ui
                )
            )
        return CvAllData(boxes=boxes)
