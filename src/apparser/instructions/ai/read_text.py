from apparser.ai_readers.base import AiReader
from apparser.base import Ui
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.ai.text_getter import GetText


class PrintAllText(AiInstruction):
    def __init__(self, text_getter: GetText = GetText()):
        self.__text_getter = text_getter

    def perform(self, ui: Ui, ai: AiReader):
        self.__text_getter.perform(ui, ai)
        for i in self.__text_getter.answer:
            points_stroke = ""
            for j in i.coordinates:
                points_stroke += str(j) + " "
            print(f'text: "{i.text}", coordinates: {points_stroke}')
