from __future__ import annotations

from typing import Any

import pytest

from apparser.instructions.ui.algorithms.algorithm import Algorithm
from tests.utils import FakeDebugger, FakeInstruction, FakeUi


def test_algorithm_rejects_invalid_debugger() -> None:
    with pytest.raises(TypeError):
        Algorithm([], debugger="debugger")


def test_algorithm_uses_default_debugger_when_requested(monkeypatch: pytest.MonkeyPatch) -> None:
    debugger = FakeDebugger()
    instruction = FakeInstruction(1)
    monkeypatch.setattr("apparser.instructions.ui.algorithms.algorithm.Debugger", lambda: debugger)
    algorithm = Algorithm([instruction], debugger=True)

    algorithm.perform(FakeUi())

    assert debugger.clear_calls == 1
    assert debugger.try_calls[0]["instruction"] is instruction


def test_algorithm_performs_instructions_without_debugger() -> None:
    instruction = FakeInstruction(1)
    ui = FakeUi()
    algorithm = Algorithm([instruction], debugger=False)

    algorithm.perform(ui)

    assert ui.window.to_foreground_calls == 1
    assert instruction.calls == [{"args": (ui,), "kwargs": {}}]


def test_algorithm_rejects_invalid_instruction_on_perform() -> None:
    algorithm = Algorithm([FakeInstruction(2000)], debugger=False)

    with pytest.raises(TypeError):
        algorithm.perform(FakeUi())


def test_algorithm_add_instruction_validates_type() -> None:
    algorithm = Algorithm([], debugger=False)

    with pytest.raises(TypeError):
        algorithm.add_instruction(object())


def test_algorithm_add_instruction_appends_instruction() -> None:
    algorithm = Algorithm([], debugger=False)
    instruction = FakeInstruction(1)

    algorithm.add_instruction(instruction)

    assert algorithm.instructions == [instruction]
