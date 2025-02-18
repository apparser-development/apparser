from base import Point
from instructions.default.base import Instruction


class MoveTo(Instruction):
    def __init__(self, coordinates: Point):
        self.__coordinates = coordinates

    def perform(self, ui):
        pass


class MoveOn(Instruction):
    def __init__(self, coordinates: Point):
        self.__coordinates = coordinates

    def perform(self, ui):
        pass
