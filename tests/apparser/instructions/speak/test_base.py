from __future__ import annotations

import pytest

from apparser.instructions.speak.base import SpeakInstruction


def test_speak_instruction_is_abstract() -> None:
    with pytest.raises(TypeError):
        SpeakInstruction()
