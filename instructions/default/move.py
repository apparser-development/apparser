from dataclasses import dataclass

from instructions.default.base import Instruction
from base import Point


@dataclass
class MoveTo(Instruction):
    cords: Point


@dataclass
class MoveOn(Instruction):
    cords: Point