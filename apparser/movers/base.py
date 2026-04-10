import abc

from apparser.geometry import Point


class BaseMover(abc.ABC):
    @abc.abstractmethod
    def move(self, position: Point):
        pass