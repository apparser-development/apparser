from types import ModuleType

from tests.utils.stubs.text.easy_ocr_reader_stub import EasyOcrReaderStub


class EasyOcrStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("easyocr")
        self.reset()

    def reset(self) -> None:
        EasyOcrReaderStub.instances = []
        self.Reader = EasyOcrReaderStub
