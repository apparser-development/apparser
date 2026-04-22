from apparser.text_readers.base import BaseTextReader
from apparser.core import BaseUi
from apparser.instructions.ocr.base import OCRInstruction
from apparser.instructions.ocr.text_getter import GetText


class PrintAllText(OCRInstruction):
    def __init__(self, text_getter: GetText = GetText()):
        self.__text_getter = text_getter

    @property
    def id(self) -> int:
        return 103

    def perform(self, ui: BaseUi, text_reader: BaseTextReader, *args, **kwargs):
        self.__text_getter.perform(ui, text_reader)
        for i in self.__text_getter.global_answer:
            points_stroke = ""
            for j in i.coordinates:
                points_stroke += str(j) + " "
            print(f'text: "{i.text}", coordinates: {points_stroke}')
