from __future__ import annotations

from typing import Any

import numpy
import pytest

from apparser.instructions.default.say_audio import SayAudio
from tests.utils import sounddevice_stub


@pytest.mark.parametrize(
    ("kwargs", "error_type"),
    [
        ({"sample_rate": "rate"}, TypeError),
        ({"sample_rate": 0}, ValueError),
        ({"blocking": "yes"}, TypeError),
        ({"microphone_device": object()}, TypeError),
        ({"audio": numpy.zeros((1, 1, 1), dtype=numpy.float32)}, ValueError),
        ({"audio": []}, ValueError),
    ],
)
def test_say_audio_validates_arguments(
    kwargs: dict[str, Any],
    error_type: type[Exception],
) -> None:
    default_kwargs = {"audio": [0.1, 0.2]}
    default_kwargs.update(kwargs)

    with pytest.raises(error_type):
        SayAudio(**default_kwargs)


def test_say_audio_requires_microphone_device() -> None:
    instruction = SayAudio(audio=[0.1, 0.2])

    with pytest.raises(ValueError):
        instruction.perform()


def test_say_audio_checks_output_and_plays_audio() -> None:
    instruction = SayAudio(audio=[0.1, 0.2], microphone_device=7, blocking=False)

    instruction.perform(mapping=[1])

    assert sounddevice_stub.check_output_settings_calls[0]["device"] == 7
    assert sounddevice_stub.play_calls[0]["device"] == 7
    assert sounddevice_stub.play_calls[0]["blocking"] is False
