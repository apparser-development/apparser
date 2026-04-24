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

import apparser.speakers.chattts as chattts_module
import apparser.speakers.torch as torch_module
from apparser.speakers.base import BaseSpeaker
from apparser.speakers.chattts import ChatTTSSpeaker
from apparser.speakers.torch import TorchSpeaker


class FakeTorchModule:
    def __init__(self):
        self.device_calls = []
        self.hub_calls = []
        self.model = None
        self.audio = None

        class _Hub:
            pass

        self.hub = _Hub()
        self.hub.load = self._load

    def device(self, value):
        self.device_calls.append(value)
        return f"device:{value}"

    def _load(self, **kwargs):
        self.hub_calls.append(kwargs)

        class FakeAudio:
            def __init__(self, data):
                self.data = numpy.asarray(data)

            def detach(self):
                return self

            def cpu(self):
                return self

            def numpy(self):
                return self.data

        class FakeModel:
            def __init__(self, owner):
                self.owner = owner
                self.to_calls = []
                self.tts_calls = []

            def to(self, device):
                self.to_calls.append(device)

            def apply_tts(self, **settings):
                self.tts_calls.append(settings)
                return FakeAudio(self.owner.audio)

        self.model = FakeModel(self)
        return self.model, None


class FakeChatTTSModule:
    def __init__(self):
        owner = self

        class InferCodeParams:
            def __init__(self, spk_emb=None):
                self.spk_emb = spk_emb

        class Chat:
            def __init__(self):
                self.load_calls = []
                self.infer_calls = []
                self.result = []
                self.sample_calls = 0
                owner.chat = self

            def load(self, **kwargs):
                self.load_calls.append(kwargs)

            def sample_random_speaker(self):
                self.sample_calls += 1
                return "random-speaker"

            def infer(self, text, params_infer_code=None, **kwargs):
                self.infer_calls.append((text, params_infer_code, kwargs))
                return self.result

        Chat.InferCodeParams = InferCodeParams
        self.Chat = Chat
        self.chat = None


def test_base_speaker_is_abstract():
    with pytest.raises(TypeError):
        BaseSpeaker()


def test_torch_speaker_init_and_speak(monkeypatch):
    fake_torch = FakeTorchModule()
    monkeypatch.setattr(torch_module.importlib, "import_module", lambda name: fake_torch)

    fake_torch.audio = numpy.array([0.1, 0.2], dtype=numpy.float32)
    speaker = TorchSpeaker(
        language="en",
        speaker_model="v4_en",
        speaker="alex",
        sample_rate=22050,
        device="cuda",
        repo_or_dir="repo",
        model="model",
        source="local",
        trust_repo=True,
        skip_validation=False,
        foo="bar",
    )
    audio = speaker.speak("hello", pitch=2)

    assert fake_torch.hub_calls == [
        {
            "repo_or_dir": "repo",
            "model": "model",
            "language": "en",
            "speaker": "v4_en",
            "source": "local",
            "foo": "bar",
            "trust_repo": True,
            "skip_validation": False,
        }
    ]
    assert fake_torch.device_calls == ["cuda"]
    assert fake_torch.model.to_calls == ["device:cuda"]
    assert fake_torch.model.tts_calls == [
        {
            "text": "hello",
            "speaker": "alex",
            "sample_rate": 22050,
            "pitch": 2,
        }
    ]
    assert numpy.array_equal(audio, numpy.array([0.1, 0.2], dtype=numpy.float32))


def test_chattts_speaker_init_uses_random_speaker(monkeypatch):
    fake_chattts = FakeChatTTSModule()
    fake_torch = FakeTorchModule()
    monkeypatch.setattr(
        chattts_module.importlib,
        "import_module",
        lambda name: {"ChatTTS": fake_chattts, "torch": fake_torch}[name],
    )

    ChatTTSSpeaker(
        source="huggingface",
        force_redownload=True,
        compile=True,
        custom_path="model-path",
        device="cpu",
        coef="coef",
        use_flash_attn=True,
        use_vllm=True,
        experimental=True,
        enable_cache=False,
    )

    assert fake_torch.device_calls == ["cpu"]
    assert fake_chattts.chat.load_calls == [
        {
            "source": "huggingface",
            "force_redownload": True,
            "compile": True,
            "custom_path": "model-path",
            "device": "device:cpu",
            "coef": "coef",
            "use_flash_attn": True,
            "use_vllm": True,
            "experimental": True,
            "enable_cache": False,
        }
    ]
    assert fake_chattts.chat.sample_calls == 1


def test_chattts_speaker_speak_creates_default_params(monkeypatch):
    fake_chattts = FakeChatTTSModule()
    fake_torch = FakeTorchModule()
    monkeypatch.setattr(
        chattts_module.importlib,
        "import_module",
        lambda name: {"ChatTTS": fake_chattts, "torch": fake_torch}[name],
    )

    speaker = ChatTTSSpeaker(speaker="voice")
    fake_chattts.chat.result = [
        numpy.array([0.1], dtype=numpy.float32),
        numpy.array([0.2, 0.3], dtype=numpy.float32),
    ]
    audio = speaker.speak("hello", temperature=0.5)

    params = fake_chattts.chat.infer_calls[0][1]

    assert params.spk_emb == "voice"
    assert fake_chattts.chat.infer_calls[0][0] == "hello"
    assert fake_chattts.chat.infer_calls[0][2] == {"temperature": 0.5}
    assert numpy.array_equal(audio, numpy.array([0.1, 0.2, 0.3], dtype=numpy.float32))


def test_chattts_speaker_speak_updates_params_and_returns_single_audio(monkeypatch):
    fake_chattts = FakeChatTTSModule()
    fake_torch = FakeTorchModule()
    monkeypatch.setattr(
        chattts_module.importlib,
        "import_module",
        lambda name: {"ChatTTS": fake_chattts, "torch": fake_torch}[name],
    )

    speaker = ChatTTSSpeaker(speaker="voice")
    params = fake_chattts.Chat.InferCodeParams()
    fake_chattts.chat.result = [numpy.array([0.4, 0.5], dtype=numpy.float32)]
    audio = speaker.speak("hello", params_infer_code=params)

    assert params.spk_emb == "voice"
    assert numpy.array_equal(audio, numpy.array([0.4, 0.5], dtype=numpy.float32))


def test_chattts_speaker_speak_returns_empty_array(monkeypatch):
    fake_chattts = FakeChatTTSModule()
    fake_torch = FakeTorchModule()
    monkeypatch.setattr(
        chattts_module.importlib,
        "import_module",
        lambda name: {"ChatTTS": fake_chattts, "torch": fake_torch}[name],
    )

    speaker = ChatTTSSpeaker(speaker="voice")
    fake_chattts.chat.result = []
    audio = speaker.speak("hello")

    assert audio.dtype == numpy.float32
    assert audio.size == 0
