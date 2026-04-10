import abc

import numpy
from appwindows import Window

from apparser.geometry import Point, RelativelyPoint


class BaseUi(abc.ABC):
    @abc.abstractmethod
    def point_to_global(self, coordinates: Point | RelativelyPoint) -> Point:
        raise NotImplementedError()

    @abc.abstractmethod
    def point_to_local(self, coordinates: Point) -> Point:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_screenshot(self) -> numpy.ndarray:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def window(self) -> Window:
        raise NotImplementedError()
