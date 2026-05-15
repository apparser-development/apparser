from __future__ import annotations

import numpy

from apparser.speakers.chat_tts import ChatTTSSpeaker
from tests.utils import chattts_stub, torch_stub


def test_chattts_speaker_initializes_dependencies() -> None:
    speaker = ChatTTSSpeaker(device="cpu", source="local")
    instance = chattts_stub.Chat.instances[0]

    assert isinstance(speaker, ChatTTSSpeaker)
    assert torch_stub.device_calls == ["cpu"]
    assert instance.load_calls[0]["source"] == "local"
    assert instance.sample_random_speaker_calls == 1


def test_chattts_speaker_uses_explicit_speaker() -> None:
    ChatTTSSpeaker(speaker="speaker-id")
    instance = chattts_stub.Chat.instances[0]

    assert instance.sample_random_speaker_calls == 0


def test_chattts_speaker_returns_empty_audio() -> None:
    chattts_stub.Chat.default_infer_result = []
    speaker = ChatTTSSpeaker(speaker="speaker-id")

    result = speaker.speak("hello")

    assert numpy.array_equal(result[0], numpy.array([], dtype=numpy.float32))


def test_chattts_speaker_concatenates_multiple_chunks() -> None:
    chattts_stub.Chat.default_infer_result = [
        numpy.asarray([1.0, 2.0], dtype=numpy.float32),
        numpy.asarray([3.0], dtype=numpy.float32),
    ]
    speaker = ChatTTSSpeaker(speaker="speaker-id")

    result = speaker.speak("hello")

    assert numpy.array_equal(result[0], numpy.asarray([1.0, 2.0, 3.0], dtype=numpy.float32))


def test_chattts_speaker_sets_missing_speaker_on_custom_params() -> None:
    chattts_stub.Chat.default_infer_result = [numpy.asarray([1.0], dtype=numpy.float32)]
    speaker = ChatTTSSpeaker(speaker="speaker-id")

    class Params:
        def __init__(self) -> None:
            self.spk_emb = None

    params = Params()

    speaker.speak("hello", params_infer_code=params)

    instance = chattts_stub.Chat.instances[0]
    assert params.spk_emb == "speaker-id"
    assert instance.infer_calls[0]["params_infer_code"] is params
