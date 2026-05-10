from __future__ import annotations

import pytest

from apparser.instructions.ocr.base import OCRInstruction


def test_ocr_instruction_is_abstract() -> None:
    with pytest.raises(TypeError):
        OCRInstruction()
