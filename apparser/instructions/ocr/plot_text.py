from typing import Tuple

from PIL import ImageDraw, Image

from apparser.core import BaseUi
from apparser.geometry import Point

from apparser.text_readers import BaseTextReader, TextData

from apparser.instructions.ocr.base import OCRInstruction
from apparser.instructions.ocr.text_getter import GetText


class _Painter:
    """Draw OCR results on top of an image."""

    def __init__(self, draw: ImageDraw.Draw, color: Tuple[int, int, int, int],
                 text_move: Point = Point(0, 20)):
        """Initialize a painter for OCR overlays.

        :param draw: Pillow drawing context.
        :type draw: ImageDraw.Draw
        :param color: RGBA color used for rendered overlays.
        :type color: Tuple[int, int, int, int]
        """
        self.__draw = draw
        self.__color = color
        self.__text_move = text_move

    def draw(self, bboxes: list[TextData]):
        for data in bboxes:
            self.__paint_cords(data)
            self.__paint_lines(data)

    def __paint_lines(self, data: TextData):
        shape = [(data.coordinates.left_top.x, data.coordinates.left_top.y), (data.coordinates.right_bottom.x, data.coordinates.right_bottom.y)]
        self.__draw.rectangle(shape, outline=self.__color, width=1)

    def __paint_cords(self, data: TextData):
        y = data.coordinates.left_top.y + self.__text_move.y
        if y < 0:
            y = data.coordinates.right_bottom.y - self.__text_move.y
        x = data.coordinates.left_top.x + self.__text_move.x
        if x < 0:
            x = data.coordinates.right_bottom.x - self.__text_move.x
        self.__draw.text((x, y), data.text, fill=self.__color)


class PlotAllText(OCRInstruction):
    """Render detected text boxes on a screenshot."""

    def __init__(self, text_getter: GetText | None = None,
                 color_rgba: tuple[int, int, int, int] = (255, 255, 255, 255),
                 text_move: Point = Point(0, 20)):
        """Initialize an OCR plotting instruction.

        :param text_getter: Instruction used to extract text from the screen. If None use GetText()
        :type text_getter: GetText | None
        :param color_rgba: RGBA color used for the rendered overlays.
        :type color_rgba: tuple[int, int, int, int]
        """
        if text_getter is None:
            text_getter = GetText()

        self.__text_getter = text_getter
        self.__color = color_rgba
        self.__text_move = text_move

    @property
    def id(self) -> int:
        return 2004

    def perform(self, ui: BaseUi, text_reader: BaseTextReader, *args, **kwargs):
        self.__text_getter.perform(ui, text_reader)
        texts = self.__text_getter.global_answer
        image = self.__text_getter.screenshot
        image = Image.fromarray(image)
        draw = ImageDraw.Draw(image)
        painter = _Painter(draw, self.__color, self.__text_move)
        painter.draw(texts)
        image.show()
