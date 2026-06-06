import numpy
import importlib 

from apparser.geometry import Point, QuadPoints
from apparser.text_readers.detectors.base import BaseTextDetector


class CraftDetector(BaseTextDetector):
    def __init__(self, cuda=False, refine=True, **kwargs):
        craft = importlib.import_module("craft_text_detector")
        self.__detector = craft.Craft(
            cuda=cuda,
            refine=refine,
            **kwargs
        )

    def read_image(self, image: numpy.ndarray) -> list[QuadPoints]:
        boxes = self.__detector.detect(image)
        result = []
        for box in boxes:
            left_top = Point(float(box[0][0]), float(box[0][1]))
            right_top = Point(float(box[1][0]), float(box[1][1]))
            right_bottom = Point(float(box[2][0]), float(box[2][1]))
            left_bottom = Point(float(box[3][0]), float(box[3][1]))
            result.append(
                QuadPoints(left_top, right_top, right_bottom, left_bottom)
            )
        return result