from __future__ import annotations

import pytest

from apparser.exceptions import DebugException
from apparser.instructions.debuggers.default import Debugger
from tests.utils import FakeInstruction


def test_debugger_executes_instruction() -> None:
    instruction = FakeInstruction()
    debugger = Debugger()

    debugger.try_perform(instruction, 1, key="value")

    assert instruction.calls == [{"args": (1,), "kwargs": {"key": "value"}}]


def test_debugger_wraps_debug_exception() -> None:
    instruction = FakeInstruction(raised_exception=DebugException("boom"))
    debugger = Debugger()

    with pytest.raises(DebugException):
        debugger.try_perform(instruction)


def test_debugger_wraps_generic_exception() -> None:
    instruction = FakeInstruction(raised_exception=ValueError("boom"))
    debugger = Debugger()

    with pytest.raises(DebugException):
        debugger.try_perform(instruction)


def test_debugger_clears_context() -> None:
    debugger = Debugger()

    debugger.clear_context()
