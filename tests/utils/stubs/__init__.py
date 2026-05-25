from tests.utils.stubs.audio.sounddevice_stub import SoundDeviceStub
from tests.utils.stubs.display.screeninfo_stub import ScreenInfoStub
from tests.utils.stubs.input.keyboard_stub import KeyboardStub
from tests.utils.stubs.input.pyautogui import PyAutoGuiFake
from tests.utils.stubs.ml.chat_stub import ChatStub
from tests.utils.stubs.ml.chattts_stub import ChatTTSStub
from tests.utils.stubs.ml.fake_torch_hub import FakeTorchHub
from tests.utils.stubs.ml.fake_torch_model import FakeTorchModel
from tests.utils.stubs.ml.fake_torch_tensor import FakeTorchTensor
from tests.utils.stubs.ml.infer_code_params import InferCodeParams
from tests.utils.stubs.ml.torch_stub import TorchStub
from tests.utils.stubs.text.easy_ocr_reader_stub import EasyOcrReaderStub
from tests.utils.stubs.text.easy_ocr_stub import EasyOcrStub
from tests.utils.stubs.text.fuzz_namespace import FuzzNamespace
from tests.utils.stubs.text.paddle_ocr_reader_stub import PaddleOcrReaderStub
from tests.utils.stubs.text.paddle_ocr_stub import PaddleOcrStub
from tests.utils.stubs.text.thefuzz_stub import TheFuzzStub
from tests.utils.stubs.vision.stub_yolo import StubYolo
from tests.utils.stubs.vision.ultralytics_stub import UltralyticsStub

__all__ = [
    "ChatStub",
    "ChatTTSStub",
    "EasyOcrReaderStub",
    "EasyOcrStub",
    "FakeTorchHub",
    "FakeTorchModel",
    "FakeTorchTensor",
    "FuzzNamespace",
    "InferCodeParams",
    "KeyboardStub",
    "PyAutoGuiFake",
    "PaddleOcrReaderStub",
    "PaddleOcrStub",
    "ScreenInfoStub",
    "SoundDeviceStub",
    "StubYolo",
    "TheFuzzStub",
    "TorchStub",
    "UltralyticsStub",
]
