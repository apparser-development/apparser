from apparser.ai_readers.base import AiReader
from apparser.base import Ui, Point, RelativelyPoint
from apparser.instructions.ai.text_moves.move_to_similar_text import MoveToSimilarText
from apparser.instructions.default import MouseClick
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.ai.text_getter import GetText
from apparser.key_codes import RightClick, LeftClick


class ClickOnSimilarText(AiInstruction):
    def __init__(self, text: str,
                 click_type: RightClick | LeftClick = LeftClick(),
                 offset: Point | RelativelyPoint = Point(0, 0),
                 text_getter = GetText()):
        self.__mouse_mover = MoveToSimilarText(text, offset, text_getter)
        self.__click_type = click_type

    def perform(self, ui: Ui, ai: AiReader):
        self.__mouse_mover.perform(ui, ai)
        MouseClick(self.__click_type)
