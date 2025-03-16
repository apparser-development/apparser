import numpy

from ai_readers.base import AiReader
from base import Ui
from instructions.ai.base import AiInstruction


class ClickOnText(AiInstruction):
    def __init__(self, text: str):
        if isinstance(text, str):
            raise ValueError("Text must be a string")

        self.__text = text

    def __call__(self, ui: Ui, ai: AiReader):
        image = numpy.array(ui.get_screenshot())
        texts = ai.read_image(image)
