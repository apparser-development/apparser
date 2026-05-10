from __future__ import annotations

from apparser import instructions


def test_instructions_exports_expected_symbols() -> None:
    assert hasattr(instructions, "BaseInstruction")
    assert hasattr(instructions, "MouseClick")
    assert hasattr(instructions, "MouseClickTo")
    assert hasattr(instructions, "Algorithm")
