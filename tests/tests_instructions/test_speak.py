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

import apparser.instructions.speak.play_text as play_text_module
import apparser.instructions.speak.say_text as say_text_module
from apparser.instructions.speak.play_text import PlayTextAudio
from apparser.instructions.speak.say_text import SayTextAudio
from apparser.speakers import BaseSpeaker
from tests.utils.ui import InteractionUi


class FakeSpeaker(BaseSpeaker):
    def __init__(self, audio):
        self.audio = numpy.asarray(audio, dtype=numpy.float32)
        self.calls = []

    def speak(self, text: str) -> numpy.ndarray:
        self.calls.append(text)
        return self.audio


@pytest.mark.parametrize("instruction_class", [PlayTextAudio, SayTextAudio])
def test_speak_instruction_validation(instruction_class):
    with pytest.raises(TypeError, match="text must be a string"):
        instruction_class(1)

    with pytest.raises(ValueError, match="text cannot be empty"):
        instruction_class("")


def test_play_text_audio_perform(monkeypatch):
    calls = []

    class FakePlayAudio:
        def __init__(self, **kwargs):
            calls.append(("init", kwargs))

        def perform(self, *args, **kwargs):
            calls.append(("perform", args, kwargs))

    monkeypatch.setattr(play_text_module, "PlayAudio", FakePlayAudio)

    speaker = FakeSpeaker([0.1, 0.2])
    instruction = PlayTextAudio("hello", sample_rate=24000, device="speaker", blocking=False)
    instruction.perform(InteractionUi(), speaker, "arg", key="value")

    kwargs = calls[0][1]

    assert speaker.calls == ["hello"]
    assert calls[0][0] == "init"
    assert numpy.allclose(kwargs["audio"], numpy.array([0.1, 0.2], dtype=numpy.float32))
    assert kwargs["sample_rate"] == 24000
    assert kwargs["device"] == "speaker"
    assert kwargs["blocking"] is False
    assert calls[1] == ("perform", ("arg",), {"key": "value"})


def test_say_text_audio_perform(monkeypatch):
    calls = []

    class FakeSayAudio:
        def __init__(self, **kwargs):
            calls.append(("init", kwargs))

        def perform(self, *args, **kwargs):
            calls.append(("perform", args, kwargs))

    monkeypatch.setattr(say_text_module, "SayAudio", FakeSayAudio)

    speaker = FakeSpeaker([0.1, 0.2])
    instruction = SayTextAudio(
        "hello",
        sample_rate=24000,
        microphone_device="microphone",
        blocking=False,
    )
    instruction.perform(InteractionUi(), speaker, "arg", key="value")

    kwargs = calls[0][1]

    assert speaker.calls == ["hello"]
    assert calls[0][0] == "init"
    assert numpy.allclose(kwargs["audio"], numpy.array([0.1, 0.2], dtype=numpy.float32))
    assert kwargs["sample_rate"] == 24000
    assert kwargs["microphone_device"] == "microphone"
    assert kwargs["blocking"] is False
    assert calls[1] == ("perform", ("arg",), {"key": "value"})
