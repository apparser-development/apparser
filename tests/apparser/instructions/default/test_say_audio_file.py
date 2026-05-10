from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import numpy
import pytest

from apparser.instructions.default.say_audio_file import SayAudioFile
from tests.utils import create_temp_audio_path, create_wave_file


def test_say_audio_file_validates_path_type() -> None:
    with pytest.raises(TypeError):
        SayAudioFile(1)


@pytest.mark.parametrize("path", ["", "missing.wav"])
def test_say_audio_file_validates_path_value(path: str) -> None:
    with pytest.raises(ValueError):
        SayAudioFile(path)


def test_say_audio_file_reads_audio_and_builds_instruction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    file_path = create_wave_file(
        create_temp_audio_path("audio.wav"),
        b"\x00\x00\xff\x7f",
        sample_width=2,
        sample_rate=16_000,
    )
    created: list[dict[str, Any]] = []

    def fake_say_audio(**kwargs: Any) -> SimpleNamespace:
        created.append({"init": kwargs})
        return SimpleNamespace(perform=lambda *args, **kwargs2: created.append({"perform": kwargs2}))

    monkeypatch.setattr("apparser.instructions.default.say_audio_file.SayAudio", fake_say_audio)
    instruction = SayAudioFile(str(file_path), microphone_device=5)

    instruction.perform(loop=True)

    assert created[0]["init"]["sample_rate"] == 16_000
    assert created[0]["init"]["microphone_device"] == 5
    assert numpy.allclose(created[0]["init"]["audio"], numpy.asarray([0.0, 0.9999695], dtype=numpy.float32))
    assert created[1] == {"perform": {"loop": True}}


def test_say_audio_file_rejects_unsupported_sample_width() -> None:
    file_path = create_wave_file(create_temp_audio_path("audio.wav"), b"\x00\x00\x00", sample_width=3)

    with pytest.raises(ValueError):
        SayAudioFile(str(file_path))
