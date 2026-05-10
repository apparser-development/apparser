from types import ModuleType

from tests.utils.stubs.text.paddle_ocr_reader_stub import PaddleOcrReaderStub


class PaddleOcrStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("paddleocr")
        self.reset()

    def reset(self) -> None:
        PaddleOcrReaderStub.instances = []
        self.PaddleOCR = PaddleOcrReaderStub
