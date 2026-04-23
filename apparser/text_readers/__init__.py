from apparser.text_readers.base import BaseTextReader
from apparser.text_readers.screens_controller import ScreensController
from apparser.text_readers.models.text_data import TextData
from apparser.text_readers.easy_ocr import EasyOcrReader
from apparser.text_readers.paddle_ocr import PaddleTextReader
from apparser.text_readers.white_black_reader import WhiteBlackReader


__all__ = ["EasyOcrReader",
           "PaddleTextReader",
           "ScreensController",
           "BaseTextReader",
           "WhiteBlackReader",
           "TextData"]
