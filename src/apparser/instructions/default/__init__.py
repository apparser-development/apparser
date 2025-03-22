from apparser.instructions.default.click import MouseClickTo, MouseClick
from apparser.instructions.default.move import MoveOn, MoveTo
from apparser.instructions.default.press import PressKey, PressKeysCombination
from apparser.instructions.default.scroll import ScrollOn
from apparser.instructions.default.sleep import Sleep
from apparser.instructions.default.algorithm import InstructionsAlgorithm

__all__ = ["PressKey",
           "PressKeysCombination",
           "MoveOn",
           "MoveTo",
           "ScrollOn",
           "MouseClickTo",
           "Sleep",
           "InstructionsAlgorithm",
           "MouseClick"]
