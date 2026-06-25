import numpy
from PIL import Image

from apparser.core import BaseUi
from apparser.geometry import Point, RelativelyPoint, QuadPoints

from apparser.text_readers import BaseTextReader, TextData

from apparser.instructions.ocr.base import OCRInstruction


class GetText(OCRInstruction):
    """Read text from a selected screen region."""

    def __init__(self,
                 left_top_point: Point | RelativelyPoint = RelativelyPoint(0, 0),
                 right_bottom_point: Point | RelativelyPoint = RelativelyPoint(1, 1),
                 reload_every_try: bool = True):
        """Initialize a screen text extraction instruction.

        :param left_top_point: Top-left point of the capture area.
        :type left_top_point: Point | RelativelyPoint
        :param right_bottom_point: Bottom-right point of the capture area.
        :type right_bottom_point: Point | RelativelyPoint
        :param reload_every_try: Whether to refresh OCR data on every call.
        :type reload_every_try: bool
        """
        self.__left_top_point = left_top_point
        self.__right_bottom_point = right_bottom_point
        self.__reload_every_try = reload_every_try
        self.__local_answer = []
        self.__global_answer = []
        self.__left_top_point_local = left_top_point
        self.__screenshot = None

    @property
    def id(self) -> int:
        return 2000

    @staticmethod
    def __shift_text_coordinates(text: TextData, offset: Point) -> TextData:
        new_coordinates = QuadPoints(
            text.coordinates.left_top + offset,
            text.coordinates.right_top + offset,
            text.coordinates.right_bottom + offset,
            text.coordinates.left_bottom + offset,
        )
        return TextData(text.text, new_coordinates)

    def __shift_texts_coordinates(self, texts: list[TextData], offset: Point) -> list[TextData]:
        returned_data = []
        for text in texts:
            returned_data.append(self.__shift_text_coordinates(text, offset))
        return returned_data

    def perform(self, ui: BaseUi, text_reader: BaseTextReader, *args, **kwargs):
        if len(self.__local_answer) != 0 and not self.__reload_every_try:
            return
        right_bottom_point = ui.point_to_local(ui.point_to_global(self.__right_bottom_point))
        self.__left_top_point_local = ui.point_to_local(ui.point_to_global(self.__left_top_point))
        left_top_point_global = ui.point_to_global(self.__left_top_point_local)
        screen = Image.fromarray(ui.get_screenshot())
        screen = screen.crop((self.__left_top_point_local.x, self.__left_top_point_local.y, right_bottom_point.x,
                              right_bottom_point.y))
        screen = numpy.array(screen)
        self.__screenshot = screen
        ai_answer = text_reader.read_image(screen)
        self.__global_answer = self.__shift_texts_coordinates(ai_answer, left_top_point_global)
        self.__local_answer = self.__shift_texts_coordinates(ai_answer, self.__left_top_point_local)

    @property
    def local_answer(self) -> list[TextData]:
        """Return text coordinates in the local UI object of the last perform.

        :return: Text coordinates in the local UI object.
        :rtype: list[TextData]
        """
        return self.__local_answer

    @property
    def global_answer(self) -> list[TextData]:
        """Return global text coordinates of the last perform.

        :return: Global text coordinates.
        :rtype: list[TextData]
        """
        return self.__global_answer

    @property
    def screenshot(self) -> numpy.ndarray:
        """Return the screenshot of the last perform.

        :return: UI screenshot.
        :rtype: numpy.ndarray
        """
        return self.__screenshot
