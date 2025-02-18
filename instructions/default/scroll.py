from dataclasses import dataclass

from instructions.default.base import Instruction


@dataclass
class ScrollOn(Instruction):
    deviation: int