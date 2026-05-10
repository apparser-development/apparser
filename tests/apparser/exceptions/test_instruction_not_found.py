from __future__ import annotations

from apparser.exceptions.instruction_not_found import (
    InstructionNotFoundException,
    InstructionWithIdNotFoundException,
    InstructionWithNameNotFoundException,
)


def test_instruction_not_found_accepts_none_message() -> None:
    error = InstructionNotFoundException(None)

    assert isinstance(error, Exception)


def test_instruction_with_id_not_found_is_specialized_exception() -> None:
    error = InstructionWithIdNotFoundException(7)

    assert isinstance(error, InstructionNotFoundException)


def test_instruction_with_name_not_found_is_specialized_exception() -> None:
    error = InstructionWithNameNotFoundException("Missing")

    assert isinstance(error, InstructionNotFoundException)
