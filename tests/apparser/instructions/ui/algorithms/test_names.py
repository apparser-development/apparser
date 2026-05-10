from __future__ import annotations

from typing import Any

import pytest

from apparser.instructions.ui.algorithms.names import NamesAlgorithm, _check_instruction
from tests.utils import FakeDebugger, FakeInstruction, FakeUi


@pytest.mark.parametrize(
    ("instruction", "error_type"),
    [
        ("value", TypeError),
        (("name", "args"), TypeError),
        ((1, []), TypeError),
    ],
)
def test_check_instruction_validates_name_structure(
    instruction: Any,
    error_type: type[Exception],
) -> None:
    with pytest.raises(error_type):
        _check_instruction(instruction)


def test_names_algorithm_rejects_invalid_debugger() -> None:
    with pytest.raises(TypeError):
        NamesAlgorithm([], debugger="debugger")


def test_names_algorithm_performs_resolved_instructions_without_debugger(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    created: list[FakeInstruction] = []

    def factory(*args: Any) -> FakeInstruction:
        instruction = FakeInstruction(1)
        created.append(instruction)
        return instruction

    monkeypatch.setattr("apparser.instructions.ui.algorithms.names.get_instruction_by_name", lambda name: factory)
    ui = FakeUi()
    algorithm = NamesAlgorithm([("WriteText", ["hello"])], debugger=False)

    algorithm.perform(ui, 1, key="value")

    assert ui.window.to_foreground_calls == 1
    assert created[0].calls == [{"args": (ui, 1), "kwargs": {"key": "value"}}]


def test_names_algorithm_uses_debugger(monkeypatch: pytest.MonkeyPatch) -> None:
    debugger = FakeDebugger(call_inner=False)
    monkeypatch.setattr(
        "apparser.instructions.ui.algorithms.names.get_instruction_by_name",
        lambda name: lambda *args: FakeInstruction(1),
    )
    algorithm = NamesAlgorithm([("Click", [])], debugger=debugger)

    algorithm.perform(FakeUi())

    assert debugger.clear_calls == 1
    assert len(debugger.try_calls) == 1


def test_names_algorithm_raises_when_instruction_is_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("apparser.instructions.ui.algorithms.names.get_instruction_by_name", lambda name: None)
    algorithm = NamesAlgorithm([("Missing", [])], debugger=False)

    with pytest.raises(ValueError):
        algorithm.perform(FakeUi())


def test_names_algorithm_add_instruction_appends_value() -> None:
    algorithm = NamesAlgorithm([], debugger=False)

    algorithm.add_instruction(("Name", []))

    assert algorithm.instructions == [("Name", [])]
