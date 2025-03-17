import numpy

from ai_readers.base import AiReader
from base import Ui, Point
from instructions.default import MouseClickTo
from instructions.ai.base import AiInstruction
from key_codes import RightClick, LeftClick


class ClickOnText(AiInstruction):
    def __init__(self, text: str, click_type: RightClick | LeftClick = LeftClick()):
        self.__text = text
        self.__click_type = click_type

    def __call__(self, ui: Ui, ai: AiReader):
        image = numpy.array(ui.get_screenshot())
        texts = ai.read_image(image)
        needed_data = None
        for i in texts:
            if i.text == self.__text:
                needed_data = i

        if needed_data is None:
            raise ValueError("Text does not exist")

        y_cords = list(set([i.y for i in needed_data.coordinates]))
        x_cords = list(set([i.x for i in needed_data.coordinates]))

        x_center = round((x_cords[0] - x_cords[1]) / 2 + x_cords[1])
        y_center = round((y_cords[0] - y_cords[1]) / 2 + y_cords[1])
        print(x_center, y_center)
        MouseClickTo(Point(x_center, y_center), self.__click_type)(ui)
