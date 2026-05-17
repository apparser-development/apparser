from apparser.instructions.ocr.base import OCRInstruction
from apparser.instructions.ocr.click_on_text import ClickOnText
from apparser.instructions.ocr.move_to_text import MoveToText
from apparser.instructions.ocr.plot_text import PlotAllText
from apparser.instructions.ocr.print_all_text import PrintAllText
from apparser.instructions.ocr.text_getter import GetText
from apparser.instructions.ocr.wait_text import WaitText


__all__ = ["PrintAllText",
           "ClickOnText",
           "GetText",
           "MoveToText",
           "OCRInstruction",
           "PlotAllText",
           "WaitText"]