from __future__ import annotations

import numpy

from apparser.speakers.torch import TorchSpeaker
from tests.utils import torch_stub


def test_torch_speaker_initializes_model() -> None:
    speaker = TorchSpeaker(device="cpu", language="en", speaker_model="v3_en")

    assert isinstance(speaker, TorchSpeaker)
    assert torch_stub.device_calls == ["cpu"]
    assert torch_stub.hub_load_calls[0]["language"] == "en"
    assert torch_stub.hub_load_calls[0]["speaker"] == "v3_en"
    assert torch_stub.hub_model.to_calls == ["device:cpu"]


def test_torch_speaker_returns_numpy_audio() -> None:
    torch_stub.hub_model.result.values = numpy.asarray([0.1, 0.2], dtype=numpy.float32)
    speaker = TorchSpeaker(speaker="aidar", sample_rate=24_000, device="cpu")

    result = speaker.speak("hello", put_accent=True)

    assert numpy.array_equal(result, numpy.asarray([0.1, 0.2], dtype=numpy.float32))
    assert torch_stub.hub_model.apply_tts_calls[0] == {
        "text": "hello",
        "speaker": "aidar",
        "sample_rate": 24_000,
        "put_accent": True,
    }
