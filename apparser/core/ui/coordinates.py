import numpy
from appwindows import Window

from apparser.core.ui.base import Ui
from apparser.geometry import Point, RelativelyPoint


class CoordinatesUi(Ui):
    def __init__(self, from_ui: Ui):
        self.__from_ui = from_ui

    def point_to_global(self, coordinates: Point | RelativelyPoint) -> Point:
        raise NotImplementedError()

    def point_to_local(self, coordinates: Point) -> Point:
        raise NotImplementedError()

    def get_screenshot(self) -> numpy.ndarray:
        raise NotImplementedError()

    @property
    def window(self) -> Window:
        raise NotImplementedError()
