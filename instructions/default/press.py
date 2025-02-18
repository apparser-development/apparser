from dataclasses import dataclass

from instructions.default.base import Instruction
from key_codes.base import KeyCode


@dataclass
class PressKey(Instruction):
    key_code: KeyCode


@dataclass
class PressKeysCombination(Instruction):
    keys: list[PressKey]
    