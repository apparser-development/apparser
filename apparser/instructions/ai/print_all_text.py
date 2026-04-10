from apparser.text_readers.base import BaseTextReader
from apparser.core import BaseUi
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.ai.text_getter import GetText


class PrintAllText(AiInstruction):
    def __init__(self, text_getter: GetText = GetText()):
        self.__text_getter = text_getter

    @property
    def id(self) -> int:
        return 103

    def perform(self, ui: BaseUi, ai: BaseTextReader, *args, **kwargs):
        self.__text_getter.perform(ui, ai)
        for i in self.__text_getter.global_answer:
            points_stroke = ""
            for j in i.coordinates:
                points_stroke += str(j) + " "
            print(f'text: "{i.text}", coordinates: {points_stroke}')
