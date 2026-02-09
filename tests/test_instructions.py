from apparser import App
from apparser.geometry import Size
from apparser.text_readers import EasyOcrReader, WhiteBlackReader

from apparser.instructions import Sleep, WriteText
from apparser.instructions.ai import AiAlgorithm, ClickOnText


reader = WhiteBlackReader(reader=EasyOcrReader(["ru"]))

algotithm = AiAlgorithm([
    Sleep(1),
    ClickOnText("Поиск в", min_similarity=0.7),
    Sleep(0.1),
    WriteText("Some text")
], ai_reader=reader)

app = App("explorer.exe", "проводник", window_size=Size(800, 800))

algotithm.perform(app.ui)