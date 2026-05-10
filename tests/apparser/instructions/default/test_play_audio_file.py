from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import numpy
import pytest

from apparser.instructions.default.play_audio_file import PlayAudioFile
from tests.utils import create_temp_audio_path, create_wave_file


def test_play_audio_file_validates_path_type() -> None:
    with pytest.raises(TypeError):
        PlayAudioFile(1)


@pytest.mark.parametrize("path", ["", "missing.wav"])
def test_play_audio_file_validates_path_value(path: str) -> None:
    with pytest.raises(ValueError):
        PlayAudioFile(path)


def test_play_audio_file_reads_audio_and_builds_instruction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    file_path = create_wave_file(
        create_temp_audio_path("audio.wav"),
        bytes([0, 255]),
        sample_width=1,
        sample_rate=8_000,
    )
    created: list[dict[str, Any]] = []

    def fake_play_audio(**kwargs: Any) -> SimpleNamespace:
        created.append({"init": kwargs})
        return SimpleNamespace(perform=lambda *args, **kwargs2: created.append({"perform": kwargs2}))

    monkeypatch.setattr("apparser.instructions.default.play_audio_file.PlayAudio", fake_play_audio)
    instruction = PlayAudioFile(str(file_path), device=4, blocking=False)

    instruction.perform(volume=0.5)

    assert created[0]["init"]["sample_rate"] == 8_000
    assert created[0]["init"]["device"] == 4
    assert created[0]["init"]["blocking"] is False
    assert numpy.allclose(created[0]["init"]["audio"], numpy.asarray([-1.0, 0.9921875], dtype=numpy.float32))
    assert created[1] == {"perform": {"volume": 0.5}}


def test_play_audio_file_rejects_unsupported_sample_width() -> None:
    file_path = create_wave_file(create_temp_audio_path("audio.wav"), b"\x00\x00\x00", sample_width=3)

    with pytest.raises(ValueError):
        PlayAudioFile(str(file_path))
