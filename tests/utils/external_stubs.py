from __future__ import annotations

import sys
from tests.utils.stubs.audio.sounddevice_stub import SoundDeviceStub
from tests.utils.stubs.display.screeninfo_stub import ScreenInfoStub
from tests.utils.stubs.input.pyautogui import PyAutoGuiFake
from tests.utils.stubs.ml.chattts_stub import ChatTTSStub
from tests.utils.stubs.ml.torch_stub import TorchStub
from tests.utils.stubs.text.easy_ocr_stub import EasyOcrStub
from tests.utils.stubs.text.paddle_ocr_stub import PaddleOcrStub
from tests.utils.stubs.text.thefuzz_stub import TheFuzzStub
from tests.utils.stubs.vision.ultralytics_stub import UltralyticsStub


pyautogui_stub = PyAutoGuiFake()
screeninfo_stub = ScreenInfoStub()
thefuzz_stub = TheFuzzStub()
ultralytics_stub = UltralyticsStub()
sounddevice_stub = SoundDeviceStub()
easyocr_stub = EasyOcrStub()
paddleocr_stub = PaddleOcrStub()
torch_stub = TorchStub()
chattts_stub = ChatTTSStub()


def install_external_stubs() -> None:
    sys.modules["pyautogui"] = pyautogui_stub
    sys.modules["screeninfo"] = screeninfo_stub
    sys.modules["thefuzz"] = thefuzz_stub
    sys.modules["ultralytics"] = ultralytics_stub
    sys.modules["sounddevice"] = sounddevice_stub
    sys.modules["easyocr"] = easyocr_stub
    sys.modules["paddleocr"] = paddleocr_stub
    sys.modules["torch"] = torch_stub
    sys.modules["ChatTTS"] = chattts_stub


def reset_external_stubs() -> None:
    for module in [
        pyautogui_stub,
        screeninfo_stub,
        thefuzz_stub,
        ultralytics_stub,
        sounddevice_stub,
        easyocr_stub,
        paddleocr_stub,
        torch_stub,
        chattts_stub,
    ]:
        module.reset()
