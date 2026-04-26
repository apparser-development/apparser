import numpy
from PIL import Image

from apparser.core import BaseUi
from apparser.geometry import Point, RelativelyPoint
from apparser.instructions.ocr.base import OCRInstruction
from apparser.text_readers import BaseTextReader, TextData


class GetText(OCRInstruction):
    def __init__(self,
                 left_top_point: Point | RelativelyPoint = RelativelyPoint(0, 0),
                 right_bottom_point: Point | RelativelyPoint = RelativelyPoint(1, 1),
                 reload_every_try: bool = True):
        self.__left_top_point = left_top_point
        self.__right_bottom_point = right_bottom_point
        self.__reload_every_try = reload_every_try
        self.__answer = []
        self.__local_answer = []
        self.__left_top_point_global = left_top_point
        self.__screenshot = None

    @property
    def id(self) -> int:
        return 200

    def __text_coordinates_to_local(self, text: TextData) -> TextData:
        new_coordinates = []
        for point in text.coordinates:
            new_coordinates.append(point + self.__left_top_point_global)
        return TextData(text.text, new_coordinates)

    def __texts_coordinates_to_local(self, texts: list[TextData]) -> list[TextData]:
        returned_data = []
        for text in texts:
            returned_data.append(self.__text_coordinates_to_local(text))
        return returned_data

    def perform(self, ui: BaseUi, text_reader: BaseTextReader, *args, **kwargs):
        if len(self.__answer) != 0 and not self.__reload_every_try:
            return
        right_bottom_point = ui.point_to_local(ui.point_to_global(self.__right_bottom_point))
        self.__left_top_point_global = ui.point_to_local(ui.point_to_global(self.__left_top_point))
        screen = Image.fromarray(ui.get_screenshot())
        screen = screen.crop((self.__left_top_point_global.x, self.__left_top_point_global.y, right_bottom_point.x,
                              right_bottom_point.y))
        self.__screenshot = screen
        screen = numpy.array(screen)
        ai_answer = text_reader.read_image(screen)
        self.__local_answer = ai_answer.copy()
        ai_answer = self.__texts_coordinates_to_local(ai_answer)
        self.__answer = ai_answer

    @property
    def global_answer(self) -> list[TextData]:
        return self.__answer

    @property
    def local_answer(self) -> list[TextData]:
        return self.__local_answer

    @property
    def screenshot(self) -> numpy.ndarray:
        return self.__screenshot
