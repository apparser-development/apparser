import pygetwindow
from PIL import ImageGrab, Image

from base.cords import Point


class Ui:
    def __init__(self, window: pygetwindow.Window):
        self.__window = window

    def coordinates_to_global(self, coordinates: Point) -> Point:
        self.__window.activate()
        returned_point = Point(coordinates.x + self.__window.left, coordinates.y + self.__window.top)
        return returned_point

    def coordinates_to_local(self, coordinates: Point) -> Point:
        self.__window.activate()
        returned_point = Point(coordinates.x - self.__window.left, coordinates.y - self.__window.top)
        return returned_point

    def get_screenshot(self) -> Image:
        image = ImageGrab.grab((self.__window.left, self.__window.top, self.__window.right, self.__window.bottom))
        return image

    def close_window(self):
        self.__window.close()

    def set_window_size(self, width, height):
        self.__window.resizeTo(width, height)

    def to_main(self):
        self.__window.activate()
