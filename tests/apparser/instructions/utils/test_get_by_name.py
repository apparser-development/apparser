from __future__ import annotations

from typing import Any

import pytest

from apparser.exceptions import InstructionWithNameNotFoundException
from apparser.instructions.utils.get_by_name import get_instruction_by_name
from tests.utils import make_instruction_type


@pytest.mark.parametrize("instruction_name", [1, None, object()])
def test_get_instruction_by_name_rejects_invalid_type(instruction_name: Any) -> None:
    with pytest.raises(TypeError):
        get_instruction_by_name(instruction_name)


def test_get_instruction_by_name_rejects_empty_name() -> None:
    with pytest.raises(ValueError):
        get_instruction_by_name("")


def test_get_instruction_by_name_returns_matching_instruction(monkeypatch: pytest.MonkeyPatch) -> None:
    first = make_instruction_type("First", 1)
    second = make_instruction_type("Second", 2)
    monkeypatch.setattr("apparser.instructions.utils.get_by_name.get_all_instructions", lambda: [first, second])

    assert get_instruction_by_name("Second") is second


def test_get_instruction_by_name_raises_when_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("apparser.instructions.utils.get_by_name.get_all_instructions", lambda: [])

    with pytest.raises(InstructionWithNameNotFoundException):
        get_instruction_by_name("Missing")
