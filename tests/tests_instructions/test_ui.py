import sys
import types

import numpy
import pytest
from appwindows.geometry import Point, Size


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

import apparser.instructions.default.click as default_click_module
from apparser.geometry import RelativelyPoint
from apparser.instructions.ui.click import MouseClickTo
from apparser.instructions.ui.mouse_move import MouseMove
from apparser.instructions.ui.move_window import WindowMove
from apparser.instructions.ui.resize_window import WindowResize
from apparser.instructions.ui.to_window import WindowToBackground, WindowToForeground
from apparser.key_codes import LeftClick
from apparser.movers.base import BaseMover
from tests.utils.ui import InteractionUi


class DummyMover(BaseMover):
    def __init__(self):
        self.points = []

    def move(self, position: Point):
        self.points.append(position)

def test_mouse_click_to_validation_and_perform(monkeypatch):
    ui = InteractionUi()
    mover = DummyMover()
    clicks = []
    monkeypatch.setattr(default_click_module.mouse, "click", lambda: clicks.append("clicked"))

    instruction = MouseClickTo(Point(3, 4), LeftClick(), mover)
    instruction.perform(ui)

    with pytest.raises(ValueError, match="coordinates must be Point or RelativelyPoint"):
        MouseClickTo("coordinates")

    assert mover.points == [Point(3, 4)]
    assert clicks == ["clicked"]


def test_mouse_move_validation_and_perform():
    mover = DummyMover()
    ui = InteractionUi()

    with pytest.raises(TypeError, match="coordinates must be Point or RelativelyPoint"):
        MouseMove("coordinates", mover)

    with pytest.raises(TypeError, match="mover must be Mover"):
        MouseMove(Point(1, 2), "mover")

    instruction = MouseMove(RelativelyPoint(0.1, 0.2), mover)
    instruction.perform(ui)

    assert ui.global_calls == [instruction._MouseMove__coordinates]
    assert mover.points == [Point(9, 8)]


def test_move_window_validation_and_perform():
    ui = InteractionUi()

    with pytest.raises(TypeError, match="position must be of type Point"):
        WindowMove("position")

    instruction = WindowMove(Point(5, 6))
    instruction.perform(ui)

    assert ui.window.calls == [("move", Point(5, 6))]


def test_resize_window_validation_and_perform():
    ui = InteractionUi()

    with pytest.raises(TypeError, match="size must be of type Size"):
        WindowResize("size")

    instruction = WindowResize(Size(20, 30))
    instruction.perform(ui)

    assert ui.window.calls == [("resize", Size(20, 30))]


def test_to_window_instructions():
    ui = InteractionUi()

    WindowToForeground().perform(ui)
    WindowToBackground().perform(ui)

    assert ui.window.calls == [("to_foreground",), ("to_background",)]
