import numpy
from PIL.Image import Image

from apparser.ai_readers.base import AiReader
from apparser.ai_readers.text_data import TextData
from apparser.base import Ui, Point, RelativelyPoint


class GetText:
    def __init__(self,
                 left_top_point: Point | RelativelyPoint = RelativelyPoint(0, 0),
                 right_bottom_point: Point | RelativelyPoint =  RelativelyPoint(1, 1),
                 reload_every_try: bool = True):
        self.__left_top_point = left_top_point
        self.__right_bottom_point = right_bottom_point
        self.__reload_every_try = reload_every_try
        self.__answer = []
        self.__left_top_point_global = left_top_point

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

    def perform(self, ui: Ui, ai: AiReader):
        if len(self.__answer) != 0 and not self.__reload_every_try:
            return
        right_bottom_point = ui.point_to_local(ui.point_to_global(self.__right_bottom_point))
        self.__left_top_point_global  = ui.point_to_local(ui.point_to_global(self.__left_top_point))
        screen = ui.get_screenshot()
        screen = screen.crop((self.__left_top_point_global.x, self.__left_top_point_global.y, right_bottom_point.x, right_bottom_point.y))
        screen = numpy.array(screen)
        ai_answer = ai.read_image(screen)
        ai_answer = self.__texts_coordinates_to_local(ai_answer)
        self.__answer = ai_answer

    @property
    def answer(self) -> list:
        return self.__answer
