import sys
import types

import numpy
import pytest


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

import apparser.instructions.utils.get_by_name as get_by_name_module
from apparser.instructions.ocr.click_on_text import ClickOnText
from apparser.instructions.default.press import PressKey
from apparser.instructions.utils.get_by_id import get_instruction_by_id
from apparser.instructions.utils.get_by_name import get_instruction_by_name


def test_get_instruction_by_name(monkeypatch):
    class FakePressKey:
        pass

    class FakeClickOnText:
        pass

    monkeypatch.setattr(
        get_by_name_module,
        "_get_all_instructions",
        lambda: [FakePressKey, FakeClickOnText],
    )

    assert get_instruction_by_name("FakePressKey") is FakePressKey
    assert get_instruction_by_name("FakeClickOnText") is FakeClickOnText

    from apparser.exceptions import InstructionWithNameNotFoundException
    with pytest.raises(InstructionWithNameNotFoundException):
        get_instruction_by_name("None")


def test_get_instruction_by_id_validation():
    with pytest.raises(TypeError, match="id must be an integer"):
        get_instruction_by_id("1")

    with pytest.raises(ValueError, match="id must be >= 0"):
        get_instruction_by_id(-1)


def test_get_instruction_by_name_validation():
    with pytest.raises(TypeError, match="id must be an str"):
        get_instruction_by_name(1)

    with pytest.raises(ValueError, match="name is empty"):
        get_instruction_by_name("")
