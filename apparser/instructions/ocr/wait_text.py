import time

from thefuzz import fuzz

from apparser.core import BaseUi
from apparser.geometry import Point, RelativelyPoint
from apparser.exceptions import TimeoutException

from apparser.text_readers import BaseTextReader, TextData

from apparser.instructions.ocr.text_getter import GetText
from apparser.instructions.ocr.base import OCRInstruction


class WaitText(OCRInstruction):
    """Waiting for the text to appear."""

    def __init__(self, text: str,
                 min_similarity: float = 0.9,
                 text_getter: GetText | None = None,
                 interval: float | int = 1,
                 expire_time: float | None = 600):
        """Initialize a text-targeted mouse movement instruction.

        :param text: Text to wait.
        :type text: str
        :param min_similarity: Minimum similarity score required for a match.
        :type min_similarity: float        
        :param text_getter: Instruction used to extract text from the screen. If None use GetText()
        :type text_getter: GetText | None
        :param interval: The interval between text checks in seconds.
        :type interval: int | float
        :param expire_time: Maximum waiting time
        :type expire_time: int | float
        
        """
        if text_getter is None:
            text_getter = GetText()

        self.__text = text
        self.__min_similarity = min_similarity
        self.__interval = interval
        self.__expire_time = expire_time

    @property
    def id(self) -> int:
        return 2005

    def __is_needed_text(self, texts: list[TextData]) -> bool:
        for i in texts:
            if fuzz.token_sort_ratio(self.__text, i.text) / 100 > self.__min_similarity:
                return True
        return False

    def perform(self, ui: BaseUi, text_reader: BaseTextReader, *args, **kwargs):
        is_founded = False
        start_time = time.time()
        while not is_founded:
            if time.time() - start_time >= self.__expire_time:
                raise TimeoutException(self.__expire_time)

            time.sleep(self.__interval)
            data = text_reader.read_image(ui.get_screenshot())
            is_founded = self.__is_needed_text(data)

    @property
    def text(self) -> str:
        return self.__text
