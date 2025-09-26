from apparser.text_readers.base import AiReader
from apparser.text_readers.readers.easy_ocr import EasyOcrReader
from apparser.text_readers.readers.screens_controller import ScreensController
from apparser.text_readers.readers.white_black_reader import WhiteBlackReader
from apparser.text_readers.text_data import TextData

__all__ = ["EasyOcrReader",
           "ScreensController",
           "AiReader",
           "WhiteBlackReader",
           "TextData"]
