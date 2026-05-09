from apparser.text_readers.base import BaseTextReader
from apparser.core import BaseUi
from apparser.instructions.ocr.base import OCRInstruction
from apparser.instructions.ocr.text_getter import GetText


class PrintAllText(OCRInstruction):
    """Print all detected text blocks and their coordinates."""

    def __init__(self, text_getter: GetText = GetText()):
        """Initialize an OCR text printing instruction.

        :param text_getter: Instruction used to extract text from the screen.
        :type text_getter: GetText
        """
        self.__text_getter = text_getter

    @property
    def id(self) -> int:
        return 2003

    def perform(self, ui: BaseUi, text_reader: BaseTextReader, *args, **kwargs):
        self.__text_getter.perform(ui, text_reader)
        for i in self.__text_getter.global_answer:
            points_stroke = ""
            for j in i.coordinates:
                points_stroke += str(j) + " "
            print(f'text: "{i.text}", coordinates: {points_stroke}')
