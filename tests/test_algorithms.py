"""Tests for algorithm classes."""

import pytest

from apparser.instructions.ui.algorithms import Algorithm
from tests.utils.instructions import DummyInstruction
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

    with pytest.raises(TypeError, match="instruction must be BaseInstruction or UiInstruction"):
        algorithm.add_instruction("instruction")

    with pytest.raises(TypeError, match="instruction must be BaseInstruction or UiInstruction"):
        Algorithm(["instruction"], None).perform(InteractionUi())

