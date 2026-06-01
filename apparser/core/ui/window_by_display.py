from functools import singledispatchmethod

import numpy
from PIL import ImageGrab

from appwindows import Window
from appwindows.geometry import Point, Size

from apparser.core.ui.base import BaseUi
from apparser.geometry.relatively_point import RelativelyPoint


class WindowByDisplayUi(BaseUi):
    """
    Represent a window as a display-captured UI context.
    Unlike the WindowUi class, it retrieves the application's image based on its borders rather than from the graphical shell.
    """

    def __init__(self, window: Window) -> None:
        """Initialize a display-captured window UI context.

        :param window: Window instance to wrap.
        :type window: Window
        :raises TypeError: If ``window`` has an invalid type.
        """
        if not isinstance(window, Window):
            raise TypeError('window must be Window')

        self.__window = window

    @singledispatchmethod
    def point_to_global(self, coordinates: Point | RelativelyPoint) -> Point:
        """Convert window coordinates to the global screen space.

        :param coordinates: Local or relative coordinates to convert.
        :type coordinates: Point | RelativelyPoint
        :return: Converted global point.
        :rtype: Point
        """
        raise NotImplementedError()

    @point_to_global.register(Point)
    def _(self, coordinates: Point) -> Point:
        return coordinates + self.__window.get_points().left_top

    @point_to_global.register(RelativelyPoint)
    def _(self, coordinates: RelativelyPoint) -> Point:
        size: Size = self.__window.get_size()
        x = round(coordinates.x * size.width)
        y = round(coordinates.y * size.height)
        local_point = Point(x, y)
        return self.point_to_global(local_point)

    def point_to_local(self, coordinates: Point) -> Point:
        """Convert global coordinates to the window local space.

        :param coordinates: Global point to convert.
        :type coordinates: Point
        :return: Converted local point.
        :rtype: Point
        """
        return coordinates - self.__window.get_points().left_top

    def get_screenshot(self) -> numpy.ndarray:
        """Capture a screenshot of the window from the display.

        :return: Window screenshot data captured by window bounds.
        :rtype: numpy.ndarray
        """
        left_top = self.__window.get_points().left_top
        size: Size = self.__window.get_size()
        screenshot = ImageGrab.grab(
            bbox=(
                left_top.x,
                left_top.y,
                left_top.x + size.width,
                left_top.y + size.height,
            ),
            all_screens=True,
        )
        return numpy.asarray(screenshot)

    @property
    def window(self) -> Window:
        """Return the wrapped window instance.

        :return: Wrapped window.
        :rtype: Window
        """
        return self.__window
