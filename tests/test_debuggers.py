"""Tests for debugger helpers."""

import pytest

from apparser.instructions.debuggers import Debugger
from apparser.exceptions import DebugException
from tests.utils.instructions import DummyInstruction


def test_debugger_try_perform_calls_instruction():
    calls = []
    debugger = Debugger()
    instruction = DummyInstruction(calls, "instruction", instruction_id=7)

    debugger.try_perform(instruction, "ui")

    assert calls == [("instruction", "ui", (), {})]


def test_debugger_wraps_unexpected_exceptions():
    debugger = Debugger()
    instruction = DummyInstruction(
        instruction_id=5,
        error=ValueError("boom"),
    )

    with pytest.raises(DebugException) as exc_info:
        debugger.try_perform(instruction, "ui")

    message = str(exc_info.value)

    assert "0\t5\tDummyInstruction" in message
    assert "boom" in message


def test_debugger_clear_context_resets_log():
    debugger = Debugger()
    debugger.try_perform(DummyInstruction(instruction_id=1), "ui")
    debugger.clear_contex()

    with pytest.raises(DebugException) as exc_info:
        debugger.try_perform(
            DummyInstruction(instruction_id=2, error=ValueError("boom")),
            "ui",
        )

    message = str(exc_info.value)

    assert "0\t2\tDummyInstruction" in message
    assert "1\t1\tDummyInstruction" not in message
