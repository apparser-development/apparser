from __future__ import annotations

import pytest

from apparser.instructions.base import BaseInstruction


def test_base_instruction_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseInstruction()
