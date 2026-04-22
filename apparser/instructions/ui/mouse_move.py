from apparser.core import BaseUi
from apparser.geometry import Point, RelativelyPoint
from apparser.instructions.ui.base import UiInstruction
from apparser.movers import DefaultMover
from apparser.movers.base import BaseMover


class MouseMove(UiInstruction):
    def __init__(self,
                 coordinates: Point | RelativelyPoint,
                 mover: BaseMover = DefaultMover()):
        if  not (isinstance(coordinates, Point) or isinstance(coordinates, RelativelyPoint)):
            raise TypeError('coordinates must be Point or RelativelyPoint')

        if not isinstance(mover, BaseMover):
            raise TypeError('mover must be Mover')

        self.__mover = mover
        self.__coordinates = coordinates

    @property
    def id(self) -> int:
        return 20

    def perform(self, ui: BaseUi, *args, **kwargs):
        coordinates = ui.point_to_global(self.__coordinates)
        self.__mover.move(coordinates)
