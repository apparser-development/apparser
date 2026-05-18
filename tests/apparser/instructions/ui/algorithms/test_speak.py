from __future__ import annotations

import pytest

from apparser.instructions.ui.algorithms.speak import SpeakAlgorithm
from tests.utils import FakeDebugger, FakeSpeaker, FakeSpeakInstruction, FakeUi


def test_speak_algorithm_rejects_invalid_speaker() -> None:
    with pytest.raises(TypeError):
        SpeakAlgorithm([], speaker=object(), debugger=False)


def test_speak_algorithm_creates_default_speaker() -> None:
    algorithm = SpeakAlgorithm([], debugger=False)

    assert algorithm.instructions == []


def test_speak_algorithm_performs_instructions() -> None:
    instruction = FakeSpeakInstruction(3000)
    speaker = FakeSpeaker()
    ui = FakeUi()
    algorithm = SpeakAlgorithm([instruction], speaker=speaker, debugger=False)

    algorithm.perform(ui)

    assert ui.window.to_foreground_calls == 1
    assert instruction.calls == [{"args": tuple([ui]), "kwargs": {}}]


def test_speak_algorithm_uses_debugger() -> None:
    debugger = FakeDebugger(call_inner=False)
    instruction = FakeSpeakInstruction(3000)
    algorithm = SpeakAlgorithm([instruction], speaker=FakeSpeaker(), debugger=debugger)

    algorithm.perform(FakeUi())

    assert debugger.clear_calls == 1
    assert debugger.try_calls[0]["instruction"] is instruction


def test_speak_algorithm_rejects_invalid_instruction_on_perform() -> None:
    algorithm = SpeakAlgorithm([object()], speaker=FakeSpeaker(), debugger=False)

    with pytest.raises(TypeError):
        algorithm.perform(FakeUi())


def test_speak_algorithm_add_instruction_validates_type() -> None:
    algorithm = SpeakAlgorithm([], speaker=FakeSpeaker(), debugger=False)

    with pytest.raises(TypeError):
        algorithm.add_instruction(object())


def test_speak_algorithm_add_instruction_appends_instruction() -> None:
    algorithm = SpeakAlgorithm([], speaker=FakeSpeaker(), debugger=False)
    instruction = FakeSpeakInstruction(3000)

    algorithm.add_instruction(instruction)

    assert algorithm.instructions == [instruction]
