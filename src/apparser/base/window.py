import pygetwindow

from apparser.base.points.absolute import Point


class Window:
    def __init__(self, window: pygetwindow.Window):
        self.__window = window

    def close(self):
        self.__window.close()

    def to_main(self):
        self.__window.activate()

    @property
    def left_top_point(self) -> Point:
        return Point(self.__window.left, self.__window.top)

    @property
    def right_bottom_point(self) -> Point:
        return Point(self.__window.right, self.__window.bottom)

    @property
    def size(self) -> tuple[int, int]:
        return self.__window.width, self.__window.height

    @size.setter
    def size(self, new_size: tuple[int, int]):
        self.__window.resizeTo(*new_size)
