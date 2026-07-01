from apparser.core import BaseUi
from apparser.geometry import Point, RelativelyPoint
from apparser.key_codes import RightClick, LeftClick

from apparser.text_readers import BaseTextReader

from apparser.instructions.default import MouseClick, Sleep
from apparser.instructions.ocr.base import OCRInstruction
from apparser.instructions.ocr.move_to_text import MoveToText
from apparser.instructions.ocr.text_getter import GetText


class ClickOnText(OCRInstruction):
    """Move to matching text and click it."""

    def __init__(self, text: str,
                 click_type: RightClick | LeftClick = LeftClick(),
                 min_similarity: float = 0.8,
                 offset: Point | RelativelyPoint = Point(0, 0),
                 text_getter: GetText | None = None,
                 sleep_time_after_move: float = 0.1):
        """Initialize a text click instruction.

        :param text: Text to locate before clicking.
        :type text: str
        :param click_type: Mouse button to click.
        :type click_type: RightClick | LeftClick
        :param min_similarity: Minimum similarity score required for a match.
        :type min_similarity: float
        :param offset: Offset relative to the detected text center.
        :type offset: Point | RelativelyPoint
        :param text_getter: Instruction used to extract text from the screen. If None, use GetText().
        :type text_getter: GetText | None
        :param sleep_time_after_move: Delay before the click is performed.
        :type sleep_time_after_move: float
        """

        if text_getter is None:
            text_getter = GetText()

        self.__mouse_mover = MoveToText(text, min_similarity, offset, text_getter)
        self.__click_type = click_type
        self.__sleep = Sleep(sleep_time_after_move)

    @property
    def id(self) -> int:
        return 2002

    def perform(self, ui: BaseUi, ocr: BaseTextReader, *args, **kwargs):
        self.__mouse_mover.perform(ui, ocr)
        self.__sleep.perform(ui, ocr)
        MouseClick(self.__click_type).perform(ui, ocr)
