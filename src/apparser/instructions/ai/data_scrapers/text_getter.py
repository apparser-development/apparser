import numpy
from PIL.Image import Image

from apparser.ai_readers.base import AiReader
from apparser.ai_readers.text_data import TextData
from apparser.base import Ui, Point, RelativelyPoint
from apparser.instructions.ai.data_scrapers.data_scraper import AiDataScraper


class GetText(AiDataScraper):
    def __init__(self,
                 left_top_point: Point | RelativelyPoint = RelativelyPoint(0, 0),
                 right_bottom_point: Point | RelativelyPoint =  RelativelyPoint(1, 1),
                 reload_every_try: bool = False):
        self.__left_top_point = left_top_point
        self.__right_bottom_point = right_bottom_point
        self.__reload_every_try = reload_every_try
        self.__answer = []

    def __text_coordinates_to_local(self, text: TextData) -> TextData:
        new_coordinates = []
        for point in text.coordinates:
            new_coordinates.append(point + self.__left_top_point)
        return TextData(text.text, new_coordinates)

    def __texts_coordinates_to_local(self, texts: list[TextData]) -> list[TextData]:
        returned_data = []
        for text in texts:
            returned_data.append(self.__text_coordinates_to_local(text))
        return returned_data

    def __resize_image(self, image: Image, ui: Ui) -> Image:
        right_bottom_point = ui.point_to_local(ui.point_to_global(self.__right_bottom_point))
        left_top_point = ui.point_to_local(ui.point_to_global(self.__left_top_point))
        return image.crop((left_top_point.x, left_top_point.y, right_bottom_point.x, right_bottom_point.y))

    def __call__(self, ui: Ui, ai: AiReader):
        if len(self.__answer) != 0 and not self.__reload_every_try:
            return
        screen = ui.get_screenshot()
        screen = numpy.array(self.__resize_image(screen, ui))
        ai_answer = ai.read_image(screen)
        ai_answer = self.__texts_coordinates_to_local(ai_answer)
        self.__answer = ai_answer

    @property
    def answer(self) -> list:
        return self.__answer
