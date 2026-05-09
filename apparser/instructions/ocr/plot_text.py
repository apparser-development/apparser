from typing import Tuple

from PIL import ImageDraw, Image

from apparser.text_readers.base import BaseTextReader
from apparser.text_readers.models.text_data import TextData
from apparser.core import BaseUi
from apparser.instructions.ocr.base import OCRInstruction
from apparser.instructions.ocr.text_getter import GetText


class _Painter:
    """Draw OCR results on top of an image."""

    def __init__(self, draw: ImageDraw.Draw, color: Tuple[int, int, int, int]):
        """Initialize a painter for OCR overlays.

        :param draw: Pillow drawing context.
        :type draw: ImageDraw.Draw
        :param color: RGBA color used for rendered overlays.
        :type color: Tuple[int, int, int, int]
        """
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


class PlotAllText(OCRInstruction):
    """Render detected text boxes on a screenshot."""

    def __init__(self, text_getter: GetText = GetText(),
                 color_rgba: tuple[int, int, int, int] = (255, 255, 255, 255)):
        """Initialize an OCR plotting instruction.

        :param text_getter: Instruction used to extract text from the screen.
        :type text_getter: GetText
        :param color_rgba: RGBA color used for the rendered overlays.
        :type color_rgba: tuple[int, int, int, int]
        """
        self.__text_getter = text_getter
        self.__color = color_rgba

    @property
    def id(self) -> int:
        return 2004

    def perform(self, ui: BaseUi, text_reader: BaseTextReader, *args, **kwargs):
        self.__text_getter.perform(ui, text_reader)
        texts = self.__text_getter.local_answer
        image = self.__text_getter.screenshot
        image = Image.fromarray(image)
        draw = ImageDraw.Draw(image)
        painter = _Painter(draw, self.__color)
        painter.draw(texts)
        image.show()
