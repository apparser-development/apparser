from thefuzz import fuzz

from apparser.core import BaseUi
from apparser.exceptions import TextNotFoundException
from apparser.geometry import Point, RelativelyPoint
from apparser.text_readers import BaseTextReader, TextData

from apparser.instructions.ocr.base import OCRInstruction
from apparser.instructions.ocr.text_getter import GetText
from apparser.instructions.ui import MouseMove



class MoveToText(OCRInstruction):
    """Move the mouse cursor to the best matching text block."""

    def __init__(self, text: str,
                 min_similarity: float = 0.9,
                 offset: Point | RelativelyPoint = Point(0, 0),
                 text_getter: GetText | None = None):
        """Initialize a text-targeted mouse movement instruction.

        :param text: Text to locate.
        :type text: str
        :param min_similarity: Minimum similarity score required for a match.
        :type min_similarity: float
        :param offset: Offset relative to the detected text center.
        :type offset: Point | RelativelyPoint
        :param text_getter: Instruction used to extract text from the screen. If None use GetText()
        :type text_getter: GetText | None
        """
        if text_getter is None:
            text_getter = GetText()

        self.__text = text
        self.__offset = offset
        self.__text_getter = text_getter
        self.__min_similarity = min_similarity

    @property
    def id(self) -> int:
        return 2001

    def find_text(self, texts: list[TextData]) -> tuple[TextData, float]:
        similar_ratings = [fuzz.token_sort_ratio(self.text, i.text) for i in texts]
        if len(similar_ratings) < 1:
            raise TextNotFoundException(self.__min_similarity)
        max_rating = max(similar_ratings)
        return texts[similar_ratings.index(max_rating)], max_rating / 100

    def __get_local_offset(self, ui: BaseUi) -> Point:
        if isinstance(self.__offset, RelativelyPoint):
            return ui.point_to_local(ui.point_to_global(self.__offset))
        return self.__offset

    def perform(self, ui: BaseUi, text_reader: BaseTextReader, *args, **kwargs):
        self.__text_getter.perform(ui, text_reader)
        needed_data, rating = self.find_text(self.__text_getter.local_answer)
        if self.__min_similarity > rating:
            raise TextNotFoundException(self.__min_similarity)
        y_cords = [needed_data.coordinates.right_top.y, needed_data.coordinates.right_bottom.y]
        x_cords = [needed_data.coordinates.left_top.x, needed_data.coordinates.right_top.x]
        offset_point = self.__get_local_offset(ui)
        x_center = round((x_cords[0] - x_cords[1]) / 2 + x_cords[1]) + offset_point.x
        y_center = round((y_cords[0] - y_cords[1]) / 2 + y_cords[1]) + offset_point.y
        MouseMove(Point(x_center, y_center)).perform(ui)

    @property
    def text(self) -> str:
        return self.__text
