from apparser.text_readers.readers.base import BaseTextReader
from apparser.text_readers.readers.easy_ocr import EasyOcrReader
from apparser.text_readers.readers.paddle import PaddleTextReader
from apparser.text_readers.readers.screens_controller import ScreensController
from apparser.text_readers.readers.white_black_reader import WhiteBlackReader

__all__ = ["EasyOcrReader",
           "ScreensController",
           "BaseTextReader",
           "WhiteBlackReader",
           "PaddleTextReader"]
