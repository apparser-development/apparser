from apparser.instructions.ai.click_on_text import ClickOnText
from apparser.instructions.ai.text_moves.move_to_text import MoveToText
from apparser.instructions.ai.text_getter import GetText
from apparser.instructions.ai.read_text import PrintAllText
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.ai.plot_text import PlotAllText
from apparser.instructions.ai.text_moves.move_to_similar_text import MoveToSimilarText
from apparser.instructions.ai.click_on_similar_text import ClickOnSimilarText

__all__ = ["PrintAllText",
           "ClickOnText",
           "GetText",
           "MoveToText",
           "AiInstruction",
           "PlotAllText",
           "ClickOnSimilarText",
           "MoveToSimilarText"]
