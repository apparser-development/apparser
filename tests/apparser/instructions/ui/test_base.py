from __future__ import annotations

import pytest

from apparser.instructions.ui.base import UiInstruction


def test_ui_instruction_is_abstract() -> None:
    with pytest.raises(TypeError):
        UiInstruction()
