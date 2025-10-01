from thefuzz import fuzz

from apparser.core import Ui
from apparser.exceptions import TextNotFoundException
from apparser.geometry import Point, RelativelyPoint
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.ai.text_getter import GetText
from apparser.instructions.default import MouseMove
from apparser.text_readers.base import AiReader
from apparser.text_readers.text_data import TextData


class MoveToText(AiInstruction):
    def __init__(self, text: str,
                 min_similarity: float = 0.9,
                 offset: Point | RelativelyPoint = Point(0, 0),
                 text_getter=GetText()):
        self.__text = text
        self.__offset = offset
        self.__text_getter = text_getter
        self.__min_similarity = min_similarity

    def find_text(self, texts: list[TextData]) -> tuple[TextData, float]:
        similar_ratings = [fuzz.token_sort_ratio(self.text, i.text) for i in texts]
        max_rating = max(similar_ratings)
        return texts[similar_ratings.index(max_rating)], max_rating

    def __get_local_offset(self, ui: Ui) -> Point:
        if isinstance(self.__offset, RelativelyPoint):
            return ui.point_to_local(ui.point_to_global(self.__offset))
        return self.__offset

    def perform(self, ui: Ui, ai: AiReader):
        self.__text_getter.perform(ui, ai)
        needed_data, rating = self.find_text(self.__text_getter.global_answer)
        if self.__min_similarity > rating:
            raise TextNotFoundException(self.__min_similarity)
        y_cords = list(set([i.y for i in needed_data.coordinates]))
        x_cords = list(set([i.x for i in needed_data.coordinates]))
        offset_point = self.__get_local_offset(ui)
        x_center = round((x_cords[0] - x_cords[1]) / 2 + x_cords[1]) + offset_point.x
        y_center = round((y_cords[0] - y_cords[1]) / 2 + y_cords[1]) + offset_point.y
        MouseMove(Point(x_center, y_center)).perform(ui)

    @property
    def text(self) -> str:
        return self.__text
