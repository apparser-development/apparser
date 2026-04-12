"""Tests for algorithm classes."""

import pytest

from apparser.algorithms import AiAlgorithm, Algorithm
from tests.utils.instructions import DummyAiInstruction, DummyInstruction
from tests.utils.readers import FakeTextReader
from tests.utils.ui import InteractionUi


def test_algorithm_perform_and_add_instruction():
    calls = []
    ui = InteractionUi()
    first = DummyInstruction(calls, "first")
    second = DummyInstruction(calls, "second")
    algorithm = Algorithm([first], None)

    algorithm.add_instruction(second)
    algorithm.perform(ui)

    assert algorithm.instructions == [first, second]
    assert ui.window.calls[0] == ("to_foreground",)
    assert [call[0] for call in calls] == ["first", "second"]


def test_algorithm_validation():
    algorithm = Algorithm([], None)

    with pytest.raises(TypeError, match="must be Instruction"):
        algorithm.add_instruction("instruction")

    with pytest.raises(TypeError, match="must be Instruction"):
        Algorithm(["instruction"], None).perform(InteractionUi())


def test_ai_algorithm_perform_and_add_instruction():
    calls = []
    ui = InteractionUi()
    ai_reader = FakeTextReader()
    first = DummyInstruction(calls, "instruction")
    second = DummyAiInstruction(calls, "ai_instruction")
    algorithm = AiAlgorithm([first], text_reader=ai_reader)

    algorithm.add_instruction(second)
    algorithm.perform(ui)

    assert algorithm.instructions == [first, second]
    assert ui.window.calls == [("to_foreground",)]
    assert calls[0][0] == "instruction"
    assert calls[1][:3] == ("ai_instruction", ui, ai_reader)


def test_ai_algorithm_validation():
    algorithm = AiAlgorithm([], text_reader=FakeTextReader())

    with pytest.raises(TypeError, match="must be Instruction or AiInstruction"):
        algorithm.add_instruction("instruction")

    with pytest.raises(TypeError, match="must be Instruction or AiInstruction"):
        AiAlgorithm(["instruction"], text_reader=FakeTextReader()).perform(
            InteractionUi()
        )
