import numpy
from PIL.Image import Image

from apparser.ai_readers.base import AiReader
from apparser.ai_readers.text_data import TextData
from apparser.base import Ui
from apparser.base.cords import Point
from apparser.instructions.ai.data_scrapers.data_scraper import AiDataScraper


class GetText(AiDataScraper):
    def __init__(self, left_top_point: Point | None = None,
                 right_bottom_point: Point | None = None,
                 reload_every_try: bool = False):
        self.__left_top_point = left_top_point
        if self.__left_top_point is None:
            self.__left_top_point = Point(0, 0)

        self.__reload_every_try = reload_every_try
        self.__right_bottom_point = right_bottom_point
        self.__answer = []

    def __resize_image(self, image: Image):
        if self.__right_bottom_point is None:
            return image

        return image.crop((self.__left_top_point.x,
                           self.__left_top_point.y,
                           self.__right_bottom_point.x,
                           self.__right_bottom_point.y))

    def __text_coordinates_to_local(self, texts: list[TextData]) -> list[TextData]:
        if self.__left_top_point == Point(0, 0):
            return texts

        returned_data = []
        for text in texts:
            new_coordinates = []
            for point in text.coordinates:
                new_coordinates.append(point + self.__left_top_point)
            new_text_data = TextData(text.text, new_coordinates)
            returned_data.append(new_text_data)
        return returned_data

    def __call__(self, ui: Ui, ai: AiReader):
        if len(self.__answer) != 0 and not self.__reload_every_try:
            return
        screen = ui.get_screenshot()
        screen = numpy.array(self.__resize_image(screen))
        ai_answer = ai.read_image(screen)
        ai_answer = self.__text_coordinates_to_local(ai_answer)
        self.__answer = ai_answer

    @property
    def answer(self) -> list:
        return self.__answer
