from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import numpy
import pytest

from apparser.instructions.speak.say_text import SayTextAudio
from tests.utils import FakeSpeaker, FakeUi


@pytest.mark.parametrize("text", [1, None])
def test_say_text_audio_rejects_invalid_text_type(text: Any) -> None:
    with pytest.raises(TypeError):
        SayTextAudio(text)


def test_say_text_audio_rejects_empty_text() -> None:
    with pytest.raises(ValueError):
        SayTextAudio("")


def test_say_text_audio_generates_audio_and_plays(monkeypatch: pytest.MonkeyPatch) -> None:
    speaker = FakeSpeaker(result=numpy.asarray([0.3, 0.4], dtype=numpy.float32))
    created: list[dict[str, Any]] = []

    def fake_say_audio(**kwargs: Any) -> SimpleNamespace:
        created.append(kwargs)
        return SimpleNamespace(perform=lambda *args, **kwargs2: created.append(kwargs2))

    monkeypatch.setattr("apparser.instructions.speak.say_text.SayAudio", fake_say_audio)
    instruction = SayTextAudio("hello", sample_rate=22_050, microphone_device=3)

    instruction.perform(FakeUi(), speaker, blocking=False)

    assert speaker.calls == ["hello"]
    assert created[0]["sample_rate"] == 22_050
    assert numpy.array_equal(created[0]["audio"], numpy.asarray([0.3, 0.4], dtype=numpy.float32))
    assert created[1] == {"blocking": False}
