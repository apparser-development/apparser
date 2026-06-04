import time

from thefuzz import fuzz

from apparser.core import BaseUi
from apparser.exceptions import TimeoutException

from apparser.text_readers import BaseTextReader, TextData

from apparser.instructions.ocr.text_getter import GetText
from apparser.instructions.ocr.base import OCRInstruction


class WaitText(OCRInstruction):
    """Wait until the target text appears."""

    def __init__(self, text: str,
                 min_similarity: float = 0.9,
                 text_getter: GetText | None = None,
                 interval: float | int = 1,
                 expire_time: float | None = 600):
        """Initialize a text waiting instruction.

        :param text: Text to wait for.
        :type text: str
        :param min_similarity: Minimum similarity score required for a match.
        :type min_similarity: float
        :param text_getter: Instruction used to extract text from the screen. If None, use GetText().
        :type text_getter: GetText | None
        :param interval: Interval between text checks in seconds.
        :type interval: int | float
        :param expire_time: Maximum waiting time in seconds. If None, wait without a timeout.
        :type expire_time: float | None
        """
        if text_getter is None:
            text_getter = GetText()

        self.__text = text
        self.__min_similarity = min_similarity
        self.__text_getter = text_getter
        self.__interval = interval
        self.__expire_time = expire_time

    @property
    def id(self) -> int:
        return 2005

    def __is_needed_text(self, texts: list[TextData]) -> bool:
        for i in texts:
            if fuzz.token_sort_ratio(self.__text, i.text) / 100 >= self.__min_similarity:
                return True
        return False

    def perform(self, ui: BaseUi, text_reader: BaseTextReader, *args, **kwargs):
        start_time = time.time()

        while True:
            self.__text_getter.perform(ui, text_reader)
            if self.__is_needed_text(self.__text_getter.local_answer):
                return

            if self.__expire_time is not None and time.time() - start_time >= self.__expire_time:
                raise TimeoutException(self.__expire_time)

            time.sleep(self.__interval)

    @property
    def text(self) -> str:
        return self.__text
