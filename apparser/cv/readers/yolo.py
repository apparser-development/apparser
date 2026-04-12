from apparser.geometry import Point, Size
from ultralytics import YOLO

from apparser import CoordinatesUi
from apparser.core import BaseUi
from apparser.cv.models import CvAllData, CvBox
from apparser.cv.readers.base import CvReader


class YoloReader(CvReader):
    def __init__(self, model: YOLO):
        self.__model = model

    def read(self, ui: BaseUi) -> CvAllData:
        results = self.__model(ui.get_screenshot())[0]
        boxes = []
        names = self.__model.model.names
        for box in results.boxes:
            cls_id = box.class_id
            cls_name = names[cls_id]
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            x = int(x1)
            y = int(y1)
            width = int(x2 - x1)
            height = int(y2 - y1)
            box_ui = CoordinatesUi(ui, Point(x ,y), Size(width, height))
            boxes.append(
                CvBox(
                    class_name=cls_name,
                    class_id=cls_id,
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    ui=box_ui
                )
            )
        return CvAllData(boxes=boxes)
