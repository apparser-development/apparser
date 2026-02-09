from apparser.text_readers.base import AiReader
from apparser.text_readers.screens_controller import ScreensController
from apparser.text_readers.text_data import TextData
from apparser.text_readers.easy_ocr import EasyOcrReader
from apparser.text_readers.white_black_reader import WhiteBlackReader


__all__ = ["EasyOcrReader",
           "ScreensController",
           "AiReader",
           "WhiteBlackReader",
           "TextData"]
