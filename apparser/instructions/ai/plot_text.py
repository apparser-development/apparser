from typing import Tuple

from PIL import ImageDraw

from apparser.text_readers.base import AiReader
from apparser.text_readers.text_data import TextData
from apparser.core import Ui
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.ai.text_getter import GetText


class _Painter:
    def __init__(self, draw: ImageDraw.Draw, color: Tuple[int, int, int, int]):
        self.__draw = draw
        self.__color = color

    def draw(self, bboxes: list[TextData]):
        for data in bboxes:
            self.__paint_cords(data)
            self.__paint_lines(data)

    def __paint_lines(self, data: TextData):
        shape = [(data.coordinates[0].x, data.coordinates[0].y), (data.coordinates[2].x, data.coordinates[2].y)]
        self.__draw.rectangle(shape, outline=self.__color, width=1)

    def __paint_cords(self, data: TextData):
        y = data.coordinates[0].y + 10
        if y < 0:
            y = data.coordinates[2].y - 10
        x = data.coordinates[0].x - 50
        if x < 0:
            x = data.coordinates[2].x + 50
        self.__draw.text((x, y), data.text, fill=self.__color)


class PlotAllText(AiInstruction):
    def __init__(self, text_getter: GetText = GetText(),
                 color_rgba: tuple[int, int, int, int] = (255, 255, 255, 255)):
        self.__text_getter = text_getter
        self.__color = color_rgba

    def perform(self, ui: Ui, ai: AiReader):
        self.__text_getter.perform(ui, ai)
        texts = self.__text_getter.local_answer
        image = self.__text_getter.screenshot
        draw = ImageDraw.Draw(image)
        painter = _Painter(draw, self.__color)
        painter.draw(texts)
        image.show()
