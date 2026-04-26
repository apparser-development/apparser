from apparser.core import BaseUi
from apparser.geometry import Point, RelativelyPoint
from apparser.instructions.default import MouseClick, Sleep
from apparser.key_codes import RightClick, LeftClick
from apparser.text_readers import BaseTextReader

from apparser.instructions.ocr.base import OCRInstruction
from apparser.instructions.ocr.move_to_text import MoveToText
from apparser.instructions.ocr.text_getter import GetText


class ClickOnText(OCRInstruction):
    def __init__(self, text: str,
                 click_type: RightClick | LeftClick = LeftClick(),
                 min_similarity: float = 0.9,
                 offset: Point | RelativelyPoint = Point(0, 0),
                 text_getter=GetText(),
                 sleep_time_before_move: float = 0.1):
        self.__mouse_mover = MoveToText(text, min_similarity, offset, text_getter)
        self.__click_type = click_type
        self.__sleep = Sleep(sleep_time_before_move)

    @property
    def id(self) -> int:
        return 202

    def perform(self, ui: BaseUi, ocr: BaseTextReader, *args, **kwargs):
        self.__mouse_mover.perform(ui, ocr)
        self.__sleep.perform(ui, ocr)
        MouseClick(self.__click_type).perform(ui, ocr)
