import abc

from apparser.geometry import Point


class Mover(abc.ABC):
    @abc.abstractmethod
    def move(self, position: Point):
        pass