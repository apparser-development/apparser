import sys
import types

import numpy


def _install_optional_dependency_stubs():
    if "torch" not in sys.modules:
        torch = types.ModuleType("torch")
        torch.device = lambda value: value

        class _Hub:
            @staticmethod
            def load(**kwargs):
                class _Model:
                    def to(self, device):
                        self.device = device

                    def apply_tts(self, **settings):
                        class _Audio:
                            def detach(self):
                                return self

                            def cpu(self):
                                return self

                            def numpy(self):
                                return numpy.array([], dtype=numpy.float32)

                        return _Audio()

                return _Model(), None

        torch.hub = _Hub()
        sys.modules["torch"] = torch

    if "ChatTTS" not in sys.modules:
        chattts = types.ModuleType("ChatTTS")

        class _Chat:
            class InferCodeParams:
                def __init__(self, spk_emb=None):
                    self.spk_emb = spk_emb

            def load(self, **kwargs):
                pass

            def sample_random_speaker(self):
                return "speaker"

            def infer(self, text, params_infer_code=None, **kwargs):
                return [numpy.array([], dtype=numpy.float32)]

        chattts.Chat = _Chat
        sys.modules["ChatTTS"] = chattts


_install_optional_dependency_stubs()

from apparser import App, BaseUi, CoordinatesUi, DesktopUi
from apparser.instructions.algorithms import AiAlgorithm, Algorithm
from apparser.core import WindowUi
from apparser.cv import DefaultCvProcess, DefaultHandlers, YoloReader
from apparser.exceptions import (
    DebugException,
    TextNotFoundException,
    WindowActionWithDesktopException,
)
from apparser.geometry import Point, RelativelyPoint, Size, distance
from apparser.instructions import (
    BaseInstruction,
    MouseClick,
    MouseClickTo,
    MouseMove,
    PressKey,
    PressKeysCombination,
    Sleep,
    WindowMove,
    WindowResize,
    WindowToBackground,
    WindowToForeground,
    WriteText,
)
from apparser.instructions.ocr import (
    OCRInstruction,
    ClickOnText,
    GetText,
    MoveToText,
    PlotAllText,
    PrintAllText,
)
from apparser.instructions.speak import PlayTextAudio, SayTextAudio, SpeakInstruction
from apparser.key_codes import (
    Alt,
    Control,
    Delete,
    Enter,
    KeyboardKeyCode,
    LeftClick,
    RightClick,
)
from apparser.movers import AntiRobotMover, DefaultMover
from apparser.text_readers import (
    BaseTextReader,
    EasyOcrReader,
    PaddleTextReader,
    ScreensController,
    TextData,
    WhiteBlackReader,
)


def test_public_imports_are_available():
    assert App is not None
    assert BaseUi is not None
    assert DesktopUi is not None
    assert CoordinatesUi is not None
    assert WindowUi is not None
    assert Point is not None
    assert Size is not None
    assert RelativelyPoint is not None
    assert distance is not None
    assert DebugException is not None
    assert TextNotFoundException is not None
    assert WindowActionWithDesktopException is not None
    assert KeyboardKeyCode is not None
    assert Enter is not None
    assert Control is not None
    assert Alt is not None
    assert Delete is not None
    assert RightClick is not None
    assert LeftClick is not None
    assert DefaultMover is not None
    assert AntiRobotMover is not None
    assert BaseInstruction is not None
    assert Algorithm is not None
    assert MouseMove is not None
    assert MouseClickTo is not None
    assert MouseClick is not None
    assert WindowMove is not None
    assert PressKey is not None
    assert PressKeysCombination is not None
    assert WindowResize is not None
    assert Sleep is not None
    assert WindowToForeground is not None
    assert WindowToBackground is not None
    assert WriteText is not None
    assert OCRInstruction is not None
    assert SpeakInstruction is not None
    assert AiAlgorithm is not None
    assert ClickOnText is not None
    assert GetText is not None
    assert MoveToText is not None
    assert PlotAllText is not None
    assert PrintAllText is not None
    assert PlayTextAudio is not None
    assert SayTextAudio is not None
    assert BaseTextReader is not None
    assert EasyOcrReader is not None
    assert PaddleTextReader is not None
    assert ScreensController is not None
    assert TextData is not None
    assert WhiteBlackReader is not None
    assert DefaultHandlers is not None
    assert DefaultCvProcess is not None
    assert YoloReader is not None
