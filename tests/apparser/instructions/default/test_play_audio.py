from __future__ import annotations

from typing import Any

import numpy
import pytest

from apparser.instructions.default.play_audio import PlayAudio
from tests.utils import sounddevice_stub


@pytest.mark.parametrize(
    ("kwargs", "error_type"),
    [
        ({"sample_rate": "rate"}, TypeError),
        ({"sample_rate": 0}, ValueError),
        ({"blocking": "yes"}, TypeError),
        ({"device": object()}, TypeError),
        ({"audio": numpy.zeros((1, 1, 1), dtype=numpy.float32)}, ValueError),
        ({"audio": []}, ValueError),
    ],
)
def test_play_audio_validates_arguments(
    kwargs: dict[str, Any],
    error_type: type[Exception],
) -> None:
    default_kwargs = {"audio": [0.1, 0.2]}
    default_kwargs.update(kwargs)

    with pytest.raises(error_type):
        PlayAudio(**default_kwargs)


def test_play_audio_checks_output_and_plays_audio() -> None:
    instruction = PlayAudio(audio=[0.1, 0.2], sample_rate=24_000, device=3, blocking=False, latency="low")

    instruction.perform()

    assert sounddevice_stub.check_output_settings_calls == [
        {
            "device": 3,
            "channels": 1,
            "dtype": "float32",
            "samplerate": 24_000,
        }
    ]
    assert sounddevice_stub.play_calls[0]["samplerate"] == 24_000
    assert sounddevice_stub.play_calls[0]["device"] == 3
    assert sounddevice_stub.play_calls[0]["blocking"] is False
    assert sounddevice_stub.play_calls[0]["latency"] == "low"


def test_play_audio_uses_mapping_to_compute_channels() -> None:
    instruction = PlayAudio(audio=[[0.1, 0.2], [0.3, 0.4]])

    instruction.perform(mapping=[2, 1], samplerate=12_000)

    assert sounddevice_stub.check_output_settings_calls[0]["channels"] == 2
    assert sounddevice_stub.check_output_settings_calls[0]["samplerate"] == 12_000
