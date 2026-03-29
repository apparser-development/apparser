import abc

import numpy
from appwindows import Window

from apparser.geometry import Point, RelativelyPoint


class Ui(abc.ABC):
    @abc.abstractmethod
    def point_to_global(self, coordinates: Point | RelativelyPoint) -> Point:
        raise NotImplementedError()

    @abc.abstractmethod
    def point_to_local(self, coordinates: Point) -> Point:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_screenshot(self) -> numpy.ndarray:
        raise NotImplementedError()

    @abc.abstractmethod
    @property
    def window(self) -> Window:
        raise NotImplementedError()
