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

import apparser.instructions.default.click as click_module
import apparser.instructions.default.play_audio as play_audio_module
import apparser.instructions.default.play_audio_file as play_audio_file_module
import apparser.instructions.default.press as press_module
import apparser.instructions.default.say_audio as say_audio_module
import apparser.instructions.default.say_audio_file as say_audio_file_module
import apparser.instructions.default.sleep as sleep_module
import apparser.instructions.default.write_text as write_text_module
from apparser.instructions.default.click import MouseClick
from apparser.instructions.default.play_audio import PlayAudio
from apparser.instructions.default.play_audio_file import PlayAudioFile
from apparser.instructions.default.press import PressKey, PressKeysCombination
from apparser.instructions.default.say_audio import SayAudio
from apparser.instructions.default.say_audio_file import SayAudioFile
from apparser.instructions.default.sleep import Sleep
from apparser.instructions.default.write_text import WriteText
from apparser.key_codes import RightClick


class FakeSoundDevice:
    def __init__(self):
        self.check_calls = []
        self.play_calls = []

    def check_output_settings(self, **kwargs):
        self.check_calls.append(kwargs)

    def play(self, audio, **kwargs):
        self.play_calls.append((audio, kwargs))


class FakeWaveReader:
    def __init__(self, samples, sample_rate=8000):
        self.samples = numpy.asarray(samples)
        self.sample_rate = sample_rate

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def getnchannels(self):
        if self.samples.ndim == 1:
            return 1
        return self.samples.shape[1]

    def getframerate(self):
        return self.sample_rate

    def getsampwidth(self):
        return self.samples.dtype.itemsize

    def getnframes(self):
        return len(self.samples)

    def readframes(self, frames):
        return self.samples.tobytes()


def test_mouse_click_validation_and_perform(monkeypatch):
    calls = []
    monkeypatch.setattr(click_module.mouse, "click", lambda: calls.append("left"))
    monkeypatch.setattr(click_module.mouse, "right_click", lambda: calls.append("right"))

    instruction = MouseClick()
    instruction.perform()
    MouseClick(RightClick()).perform()

    with pytest.raises(TypeError):
        MouseClick("click")

    assert calls == ["left", "right"]


def test_press_key_and_combination(monkeypatch):
    send_calls = []
    press_calls = []
    release_calls = []
    monkeypatch.setattr(press_module.keyboard, "send", lambda key: send_calls.append(key))
    monkeypatch.setattr(press_module.keyboard, "press", lambda key: press_calls.append(key))
    monkeypatch.setattr(press_module.keyboard, "release", lambda key: release_calls.append(key))

    instruction = PressKey("a")
    instruction.perform()
    PressKey(RightClick()).perform()
    PressKeysCombination(["ctrl", "c"]).perform()

    with pytest.raises(TypeError):
        PressKey(1)

    with pytest.raises(TypeError):
        PressKeysCombination(["ctrl", 1]).perform()

    assert send_calls == ["a", "RIGHT"]
    assert press_calls == ["ctrl", "c", "ctrl"]
    assert release_calls == ["ctrl", "c"]


def test_sleep_validation_and_perform(monkeypatch):
    sleep_calls = []
    monkeypatch.setattr(sleep_module.time, "sleep", lambda seconds: sleep_calls.append(seconds))

    with pytest.raises(ValueError):
        Sleep(0)

    instruction = Sleep(0.5)
    instruction.perform()

    assert sleep_calls == [0.5]


def test_write_text_validation_and_perform(monkeypatch):
    calls = []
    monkeypatch.setattr(write_text_module.keyboard, "write", lambda text, pause: calls.append((text, pause)))

    with pytest.raises(TypeError):
        WriteText(1)

    with pytest.raises(TypeError):
        WriteText("text", "0.1")

    with pytest.raises(ValueError):
        WriteText("")

    instruction = WriteText("hello", 0.2)
    instruction.perform()

    assert calls == [("hello", 0.2)]


@pytest.mark.parametrize(
    ("kwargs", "exception", "message"),
    [
        ({"audio": [0.1], "sample_rate": "48000"}, TypeError, "sample_rate must be a number"),
        ({"audio": [0.1], "sample_rate": 0}, ValueError, "sample_rate must be > 0"),
        ({"audio": [0.1], "blocking": "yes"}, TypeError, "blocking must be bool"),
        ({"audio": [0.1], "device": object()}, TypeError, "device must be int, str or None"),
        ({"audio": numpy.zeros((1, 1, 1))}, ValueError, "audio must be 1D or 2D array"),
        ({"audio": numpy.array([], dtype=numpy.float32)}, ValueError, "audio cannot be empty"),
        ({"audio": numpy.empty((1, 0), dtype=numpy.float32)}, ValueError, "audio cannot be empty"),
    ],
)
def test_play_audio_validation(kwargs, exception, message, monkeypatch):
    fake_sounddevice = FakeSoundDevice()
    monkeypatch.setattr(play_audio_module.importlib, "import_module", lambda name: fake_sounddevice)

    with pytest.raises(exception, match=message):
        PlayAudio(**kwargs)


def test_play_audio_perform(monkeypatch):
    fake_sounddevice = FakeSoundDevice()
    monkeypatch.setattr(play_audio_module.importlib, "import_module", lambda name: fake_sounddevice)

    instruction = PlayAudio(
        audio=[[0.1, 0.2], [0.3, 0.4]],
        sample_rate=48000,
        device="speaker",
        blocking=False,
        mapping=[1, 2],
        latency="low",
    )
    instruction.perform(samplerate=16000, device="headphones", blocking=True)

    audio, settings = fake_sounddevice.play_calls[0]

    assert fake_sounddevice.check_calls == [
        {
            "device": "headphones",
            "channels": 2,
            "dtype": "float32",
            "samplerate": 16000,
        }
    ]
    assert isinstance(audio, numpy.ndarray)
    assert audio.dtype == numpy.float32
    assert settings == {
        "samplerate": 16000,
        "device": "headphones",
        "blocking": True,
        "mapping": [1, 2],
        "latency": "low",
    }


def test_play_audio_file_validation():
    with pytest.raises(TypeError):
        PlayAudioFile(1)

    with pytest.raises(ValueError):
        PlayAudioFile("")

    with pytest.raises(ValueError):
        PlayAudioFile("missing.wav")


def test_play_audio_file_reads_audio_and_delegates(monkeypatch):
    calls = []

    class FakePlayAudio:
        def __init__(self, **kwargs):
            calls.append(("init", kwargs))

        def perform(self, *args, **kwargs):
            calls.append(("perform", args, kwargs))

    monkeypatch.setattr(play_audio_file_module, "PlayAudio", FakePlayAudio)
    monkeypatch.setattr(play_audio_file_module.pathlib.Path, "is_file", lambda self: True)
    monkeypatch.setattr(
        play_audio_file_module.wave,
        "open",
        lambda path, mode: FakeWaveReader(numpy.array([[0, 32767], [-32768, 0]], dtype=numpy.int16)),
    )

    instruction = PlayAudioFile(
        "audio.wav",
        device="speaker",
        blocking=False,
        mapping=[1, 2],
    )
    instruction.perform("arg", key="value")

    kwargs = calls[0][1]

    assert kwargs["sample_rate"] == 8000
    assert kwargs["device"] == "speaker"
    assert kwargs["blocking"] is False
    assert kwargs["mapping"] == [1, 2]
    assert kwargs["audio"].dtype == numpy.float32
    assert kwargs["audio"].shape == (2, 2)
    assert numpy.allclose(
        kwargs["audio"],
        numpy.array([[0.0, 32767 / 32768], [-1.0, 0.0]], dtype=numpy.float32),
    )
    assert calls[1] == ("perform", ("arg",), {"key": "value"})


@pytest.mark.parametrize(
    ("kwargs", "exception", "message"),
    [
        ({"audio": [0.1], "sample_rate": "48000"}, TypeError, "sample_rate must be a number"),
        ({"audio": [0.1], "sample_rate": 0}, ValueError, "sample_rate must be > 0"),
        ({"audio": [0.1], "blocking": "yes"}, TypeError, "blocking must be bool"),
        (
            {"audio": [0.1], "microphone_device": object()},
            TypeError,
            "microphone_device must be int, str or None",
        ),
        ({"audio": numpy.zeros((1, 1, 1))}, ValueError, "audio must be 1D or 2D array"),
        ({"audio": numpy.array([], dtype=numpy.float32)}, ValueError, "audio cannot be empty"),
        ({"audio": numpy.empty((1, 0), dtype=numpy.float32)}, ValueError, "audio cannot be empty"),
    ],
)
def test_say_audio_validation(kwargs, exception, message, monkeypatch):
    fake_sounddevice = FakeSoundDevice()
    monkeypatch.setattr(say_audio_module.importlib, "import_module", lambda name: fake_sounddevice)

    with pytest.raises(exception, match=message):
        SayAudio(**kwargs)


def test_say_audio_perform_uses_microphone_device(monkeypatch):
    fake_sounddevice = FakeSoundDevice()
    monkeypatch.setattr(say_audio_module.importlib, "import_module", lambda name: fake_sounddevice)

    instruction = SayAudio(
        audio=[[0.1, 0.2], [0.3, 0.4]],
        sample_rate=48000,
        microphone_device="microphone",
        blocking=False,
        mapping=[1],
        latency="low",
    )
    instruction.perform(samplerate=16000, microphone_device="override", blocking=True)

    audio, settings = fake_sounddevice.play_calls[0]

    assert fake_sounddevice.check_calls == [
        {
            "device": "override",
            "channels": 1,
            "dtype": "float32",
            "samplerate": 16000,
        }
    ]
    assert isinstance(audio, numpy.ndarray)
    assert audio.dtype == numpy.float32
    assert settings == {
        "samplerate": 16000,
        "device": "override",
        "blocking": True,
        "mapping": [1],
        "latency": "low",
    }


def test_say_audio_perform_uses_device_fallback(monkeypatch):
    fake_sounddevice = FakeSoundDevice()
    monkeypatch.setattr(say_audio_module.importlib, "import_module", lambda name: fake_sounddevice)

    instruction = SayAudio(audio=[0.1], sample_rate=48000)
    instruction.perform(device="fallback")

    assert fake_sounddevice.check_calls == [
        {
            "device": "fallback",
            "channels": 1,
            "dtype": "float32",
            "samplerate": 48000,
        }
    ]


def test_say_audio_perform_raises_without_microphone_device(monkeypatch):
    fake_sounddevice = FakeSoundDevice()
    monkeypatch.setattr(say_audio_module.importlib, "import_module", lambda name: fake_sounddevice)

    instruction = SayAudio(audio=[0.1], sample_rate=48000)

    with pytest.raises(ValueError):
        instruction.perform()


def test_say_audio_file_validation():
    with pytest.raises(TypeError):
        SayAudioFile(1)

    with pytest.raises(ValueError):
        SayAudioFile("")

    with pytest.raises(ValueError):
        SayAudioFile("missing.wav")


def test_say_audio_file_reads_audio_and_delegates(monkeypatch):
    calls = []

    class FakeSayAudio:
        def __init__(self, **kwargs):
            calls.append(("init", kwargs))

        def perform(self, *args, **kwargs):
            calls.append(("perform", args, kwargs))

    monkeypatch.setattr(say_audio_file_module, "SayAudio", FakeSayAudio)
    monkeypatch.setattr(say_audio_file_module.pathlib.Path, "is_file", lambda self: True)
    monkeypatch.setattr(
        say_audio_file_module.wave,
        "open",
        lambda path, mode: FakeWaveReader(numpy.array([0, 255], dtype=numpy.uint8)),
    )

    instruction = SayAudioFile(
        "audio.wav",
        microphone_device="microphone",
        blocking=False,
        mapping=[1],
    )
    instruction.perform("arg", key="value")

    kwargs = calls[0][1]

    assert kwargs["sample_rate"] == 8000
    assert kwargs["microphone_device"] == "microphone"
    assert kwargs["blocking"] is False
    assert kwargs["mapping"] == [1]
    assert kwargs["audio"].dtype == numpy.float32
    assert numpy.allclose(
        kwargs["audio"],
        numpy.array([-1.0, 127 / 128], dtype=numpy.float32),
    )
    assert calls[1] == ("perform", ("arg",), {"key": "value"})
