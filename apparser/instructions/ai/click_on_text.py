from apparser.core import Ui
from apparser.core.geometry import Point, RelativelyPoint
from apparser.instructions import Sleep
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.ai.move_to_text import MoveToText
from apparser.instructions.ai.text_getter import GetText
from apparser.instructions.default import MouseClick
from apparser.key_codes import RightClick, LeftClick
from apparser.text_readers.base import AiReader


class ClickOnText(AiInstruction):
    def __init__(self, text: str,
                 click_type: RightClick | LeftClick = LeftClick(),
                 min_similarity: float = 0.9,
                 offset: Point | RelativelyPoint = Point(0, 0),
                 text_getter=GetText(),
                 sleep_time_before_move: float = 0.1):
        self.__mouse_mover = MoveToText(text, min_similarity, offset, text_getter)
        self.__click_type = click_type
        self.__sleep = Sleep(sleep_time_before_move)

    def perform(self, ui: Ui, ai: AiReader):
        self.__mouse_mover.perform(ui, ai)
        self.__sleep.perform(ui, ai)
        MouseClick(self.__click_type).perform(ui, ai)
