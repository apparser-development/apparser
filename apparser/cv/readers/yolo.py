from ultralytics import YOLO
import numpy as np

from apparser.cv.models import CvAllData, CvBox
from apparser.cv.readers.base import CvReader


class YoloReader(CvReader):
    def __init__(self, **kwargs):
        self.__model = YOLO(**kwargs)

    def read(self, image: np.ndarray) -> CvAllData:
        results = self.__model(image)[0]
        boxes = []
        names = self.__model.model.names
        for box in results.boxes:
            cls_id = int(box.cls.item())
            cls_name = names[cls_id]
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            x = int(x1)
            y = int(y1)
            width = int(x2 - x1)
            height = int(y2 - y1)
            boxes.append(
                CvBox(
                    class_name=cls_name,
                    class_id=cls_id,
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                )
            )
        return CvAllData(boxes=boxes)
