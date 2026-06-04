from __future__ import annotations

from typing import Any

import pytest

from apparser.exceptions import InstructionWithIdNotFoundException
from apparser.instructions.utils.get_by_id import get_instruction_by_id
from tests.utils import make_instruction_type


@pytest.mark.parametrize("instruction_id", ["1", None, object()])
def test_get_instruction_by_id_rejects_invalid_type(instruction_id: Any) -> None:
    with pytest.raises(TypeError):
        get_instruction_by_id(instruction_id)


def test_get_instruction_by_id_rejects_negative_value() -> None:
    with pytest.raises(ValueError):
        get_instruction_by_id(-1)


def test_get_instruction_by_id_returns_matching_instruction(monkeypatch: pytest.MonkeyPatch) -> None:
    first = make_instruction_type("First", 1)
    second = make_instruction_type("Second", 2)
    monkeypatch.setattr("apparser.instructions.utils.get_by_id.get_all_instructions", lambda: [first, second])

    assert get_instruction_by_id(2) is second


def test_get_instruction_by_id_raises_when_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("apparser.instructions.utils.get_by_id.get_all_instructions", lambda: [])

    with pytest.raises(InstructionWithIdNotFoundException):
        get_instruction_by_id(1)
