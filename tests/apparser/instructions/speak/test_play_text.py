from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import numpy
import pytest

from apparser.instructions.speak.play_text import PlayTextAudio
from tests.utils import FakeSpeaker, FakeUi


@pytest.mark.parametrize("text", [1, None])
def test_play_text_audio_rejects_invalid_text_type(text: Any) -> None:
    with pytest.raises(TypeError):
        PlayTextAudio(text)


def test_play_text_audio_rejects_empty_text() -> None:
    with pytest.raises(ValueError):
        PlayTextAudio("")


def test_play_text_audio_generates_audio_and_plays(monkeypatch: pytest.MonkeyPatch) -> None:
    speaker = FakeSpeaker(result=(numpy.asarray([0.1, 0.2], dtype=numpy.float32), 16_000))
    created: list[dict[str, Any]] = []

    def fake_play_audio(**kwargs: Any) -> SimpleNamespace:
        created.append(kwargs)
        return SimpleNamespace(perform=lambda *args, **kwargs2: created.append(kwargs2))

    monkeypatch.setattr("apparser.instructions.speak.play_text.PlayAudio", fake_play_audio)
    instruction = PlayTextAudio("hello", sample_rate=16_000, device=2)

    instruction.perform(speaker, volume=0.5)

    assert speaker.calls == ["hello"]
    assert created[0]["sample_rate"] == 16_000
    assert numpy.array_equal(created[0]["audio"], numpy.asarray([0.1, 0.2], dtype=numpy.float32))
    assert created[1] == {"volume": 0.5}
