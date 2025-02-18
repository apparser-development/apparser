from base import Point


class Ui:
    def __init__(self):
        pass

    def coordinates_to_global(self, coordinates: Point) -> Point:
        pass

    def coordinates_to_local(self, coordinates: Point) -> Point:
        pass

    def get_screenshot(self):
        pass

    @property
    def window_size(self):
        return self.__window_size

    @property
    def zero_coordinates(self):
        return self.__zero_coordinates