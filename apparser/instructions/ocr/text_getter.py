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
        self.__left_top_point_global = left_top_point
        self.__screenshot = None

    @property
    def id(self) -> int:
        return 2000

    def __text_coordinates_to_local(self, text: TextData) -> TextData:
        new_coordinates = QuadPoints(
            text.coordinates.left_top + self.__left_top_point_global,
            text.coordinates.right_top + self.__left_top_point_global,
            text.coordinates.right_bottom + self.__left_top_point_global,
            text.coordinates.left_bottom + self.__left_top_point_global,
        )
        return TextData(text.text, new_coordinates)

    def __texts_coordinates_to_local(self, texts: list[TextData]) -> list[TextData]:
        returned_data = []
        for text in texts:
            returned_data.append(self.__text_coordinates_to_local(text))
        return returned_data

    def perform(self, ui: BaseUi, text_reader: BaseTextReader, *args, **kwargs):
        if len(self.__local_answer) != 0 and not self.__reload_every_try:
            return
        right_bottom_point = ui.point_to_local(ui.point_to_global(self.__right_bottom_point))
        self.__left_top_point_global = ui.point_to_local(ui.point_to_global(self.__left_top_point))
        screen = Image.fromarray(ui.get_screenshot())
        screen = screen.crop((self.__left_top_point_global.x, self.__left_top_point_global.y, right_bottom_point.x,
                              right_bottom_point.y))
        screen = numpy.array(screen)
        self.__screenshot = screen
        ai_answer = text_reader.read_image(screen)
        self.__global_answer = ai_answer.copy()
        ai_answer = self.__texts_coordinates_to_local(ai_answer)
        self.__local_answer = ai_answer

    @property
    def local_answer(self) -> list[TextData]:
        """Return the texts coordinates in local Ui object of the last perform.

        :return: Texts coordinates in local Ui object.
        :rtype: list[TextData]
        """
        return self.__local_answer

    @property
    def global_answer(self) -> list[TextData]:
        """Return the global texts coordinates of the last perform.

        :return: Global texts coordinates.
        :rtype: list[TextData]
        """
        return self.__global_answer

    @property
    def screenshot(self) -> numpy.ndarray:
        """Return the screenshot of the last perform.

        :return: Ui screenshot
        :rtype: numpy.ndarray
        """
        return self.__screenshot
