"""Reusable text-reader doubles for tests."""

from apparser.text_readers.base import BaseTextReader


class FakeTextReader(BaseTextReader):
    """Return predefined OCR results and record read calls."""

    def __init__(self, result=None):
        self.result = [] if result is None else result
        self.calls = []

    def read_image(self, image):
        self.calls.append(image)
        return self.result
