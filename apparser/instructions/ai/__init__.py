from apparser.instructions.algorithms.ai import AiAlgorithm
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.ai.click_on_text import ClickOnText
from apparser.instructions.ai.move_to_text import MoveToText
from apparser.instructions.ai.plot_text import PlotAllText
from apparser.instructions.ai.print_all_text import PrintAllText
from apparser.instructions.ai.text_getter import GetText

__all__ = ["PrintAllText",
           "ClickOnText",
           "GetText",
           "MoveToText",
           "AiInstruction",
           "PlotAllText",
           "AiAlgorithm"]
