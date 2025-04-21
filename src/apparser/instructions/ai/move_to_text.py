from apparser.ai_readers.base import AiReader
from apparser.ai_readers.text_data import TextData
from apparser.base import Ui, Point, RelativelyPoint
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.ai.text_getter import GetText
from apparser.instructions.default import MoveTo


class MoveToText(AiInstruction):
    def __init__(self, text: str,
                 offset: Point | RelativelyPoint = Point(0, 0),
                 text_getter=GetText()):
        self.__text = text
        self.__offset = offset
        self.__text_getter = text_getter

    def __find_text(self, texts: list[TextData]) -> TextData:
        needed_data = None
        for i in texts:
            if i.text == self.__text:
                needed_data = i
        if needed_data is None:
            raise ValueError("Text does not exist")
        return needed_data

    def __get_local_offset(self, ui: Ui) -> Point:
        if isinstance(self.__offset, RelativelyPoint):
            return ui.point_to_local(ui.point_to_global(self.__offset))
        return self.__offset

    def perform(self, ui: Ui, ai: AiReader):
        self.__text_getter.perform(ui, ai)
        needed_data = self.__find_text(self.__text_getter.answer)
        y_cords = list(set([i.y for i in needed_data.coordinates]))
        x_cords = list(set([i.x for i in needed_data.coordinates]))
        offset_point = self.__get_local_offset(ui)
        x_center = round((x_cords[0] - x_cords[1]) / 2 + x_cords[1]) + offset_point.x
        y_center = round((y_cords[0] - y_cords[1]) / 2 + y_cords[1]) + offset_point.y
        MoveTo(Point(x_center, y_center)).perform(ui)
