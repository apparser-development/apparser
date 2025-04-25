from apparser.ai_readers.text_data import TextData
from apparser.base import Point, RelativelyPoint
from apparser.instructions.ai.text_moves.base import TextMover
from apparser.instructions.ai.text_getter import GetText
from thefuzz import fuzz


class MoveToSimilarText(TextMover):
    def __init__(self, text: str,
                 offset: Point | RelativelyPoint = Point(0, 0),
                 text_getter=GetText()):
        super().__init__(text, offset, text_getter)

    def find_text(self, texts: list[TextData]) -> TextData:
        similar_ratings = [fuzz.token_sort_ratio(self.text, i.text) for i in texts]
        return texts[similar_ratings.index(max(similar_ratings))]