import abc

import numpy
from appwindows import Window

from apparser.geometry import Point, RelativelyPoint


class BaseUi(abc.ABC):
    """Define the common interface for UI coordinate systems."""

    @abc.abstractmethod
    def point_to_global(self, coordinates: Point | RelativelyPoint) -> Point:
        """Convert coordinates to the global screen space.

        :param coordinates: Local or relative coordinates to convert.
        :type coordinates: Point | RelativelyPoint
        :return: Converted global point.
        :rtype: Point
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def point_to_local(self, coordinates: Point) -> Point:
        """Convert coordinates to the local UI space.

        :param coordinates: Global point to convert.
        :type coordinates: Point
        :return: Converted local point.
        :rtype: Point
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_screenshot(self) -> numpy.ndarray:
        """Capture the current UI screenshot.

        :return: Screenshot data.
        :rtype: numpy.ndarray
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def window(self) -> Window:
        """Return the window associated with the UI context.

        :return: Underlying application window.
        :rtype: Window
        """
        raise NotImplementedError()
