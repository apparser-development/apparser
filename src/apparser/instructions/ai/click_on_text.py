from apparser.ai_readers.base import AiReader
from apparser.base import Ui, Point
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.ai.data_scrapers.text_getter import GetText
from apparser.instructions.default import MouseClickTo
from apparser.key_codes import RightClick, LeftClick


class ClickOnText(AiInstruction):
    def __init__(self, text: str,
                 click_type: RightClick | LeftClick = LeftClick(),
                 offset: Point = Point(0, 0),
                 text_getter=GetText()):
        self.__text = text
        self.__click_type = click_type
        self.__offset = offset
        self.__text_getter = text_getter

    def __call__(self, ui: Ui, ai: AiReader):
        self.__text_getter(ui, ai)

        needed_data = None
        for i in self.__text_getter.answer:
            if i.text == self.__text:
                needed_data = i

        if needed_data is None:
            raise ValueError("Text does not exist")

        y_cords = list(set([i.y for i in needed_data.coordinates]))
        x_cords = list(set([i.x for i in needed_data.coordinates]))

        x_center = round((x_cords[0] - x_cords[1]) / 2 + x_cords[1]) + self.__offset.x
        y_center = round((y_cords[0] - y_cords[1]) / 2 + y_cords[1]) + self.__offset.y

        MouseClickTo(Point(x_center, y_center), self.__click_type)(ui)
