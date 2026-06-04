from types import ModuleType

from tests.utils.stubs.vision.stub_yolo import StubYolo


class UltralyticsStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("ultralytics")
        self.reset()

    def reset(self) -> None:
        self.YOLO = StubYolo
