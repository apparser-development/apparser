from apparser.core import Ui
from apparser.geometry import Point, RelativelyPoint
from apparser.instructions.base import Instruction
from apparser.movers import DefaultMover
from apparser.movers.base import Mover


class MouseMove(Instruction):
    def __init__(self,
                 coordinates: Point | RelativelyPoint,
                 mover: Mover = DefaultMover()):
        if  not (isinstance(coordinates, Point) or isinstance(coordinates, RelativelyPoint)):
            raise TypeError('coordinates must be Point or RelativelyPoint')

        if not isinstance(mover, Mover):
            raise TypeError('mover must be Mover')

        self.__mover = mover
        self.__coordinates = coordinates

    def perform(self, ui: Ui, *args, **kwargs):
        coordinates = ui.point_to_global(self.__coordinates)
        self.__mover.move(coordinates)