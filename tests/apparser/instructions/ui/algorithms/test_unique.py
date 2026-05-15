from __future__ import annotations

import pytest

from apparser.instructions.ui.algorithms.unique import UniqueAlgorithm
from tests.utils import (
    FakeDebugger,
    FakeInstruction,
    FakeIntAttributeInstruction,
    FakeStrAttributeInstruction,
    FakeUi,
)


def test_unique_algorithm_rejects_invalid_debugger() -> None:
    with pytest.raises(TypeError):
        UniqueAlgorithm([], [], debugger="debugger")


def test_unique_algorithm_injects_attributes_by_type() -> None:
    first = FakeIntAttributeInstruction(1)
    second = FakeStrAttributeInstruction(2)
    ui = FakeUi()
    algorithm = UniqueAlgorithm([first, second], attributes=[10, "alex"], debugger=False)

    algorithm.perform(ui)

    assert first.calls == [{"args": (ui,), "kwargs": {"number": 10}}]
    assert second.calls == [{"args": (ui,), "kwargs": {"name": "alex"}}]


def test_unique_algorithm_uses_debugger() -> None:
    debugger = FakeDebugger(call_inner=False)
    instruction = FakeIntAttributeInstruction(1)
    algorithm = UniqueAlgorithm([instruction], attributes=[10], debugger=debugger)

    algorithm.perform(FakeUi())

    assert debugger.clear_calls == 1
    assert debugger.try_calls[0]["instruction"] is instruction


def test_unique_algorithm_rejects_invalid_instruction_on_perform() -> None:
    algorithm = UniqueAlgorithm([object()], attributes=[], debugger=False)

    with pytest.raises(TypeError):
        algorithm.perform(FakeUi())


def test_unique_algorithm_add_instruction_validates_type() -> None:
    algorithm = UniqueAlgorithm([], attributes=[], debugger=False)

    with pytest.raises(TypeError):
        algorithm.add_instruction(object())


def test_unique_algorithm_add_instruction_appends_instruction() -> None:
    algorithm = UniqueAlgorithm([], attributes=[], debugger=False)
    instruction = FakeInstruction(1)

    algorithm.add_instruction(instruction)

    assert algorithm.instructions == [instruction]
