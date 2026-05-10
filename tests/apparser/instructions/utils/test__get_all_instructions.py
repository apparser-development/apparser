import types

from apparser.instructions.base import BaseInstruction
from apparser.instructions.default.click import MouseClick
from apparser.instructions.utils._get_all_instructions import _get_all_instructions
from tests.utils import make_instruction_type


def test_get_all_instructions_collects_only_concrete_instruction_classes(
    monkeypatch,
) -> None:
    custom_instruction = make_instruction_type("CustomInstruction", 101)
    fake_default = types.SimpleNamespace(__all__=["MouseClick", "BaseInstruction", "value"], MouseClick=MouseClick, BaseInstruction=BaseInstruction, value=1)
    fake_ocr = types.SimpleNamespace(__all__=["CustomInstruction"], CustomInstruction=custom_instruction)
    fake_speak = types.SimpleNamespace(__all__=[])
    fake_ui = types.SimpleNamespace(__all__=[])
    monkeypatch.setattr("apparser.instructions.utils._get_all_instructions.default", fake_default)
    monkeypatch.setattr("apparser.instructions.utils._get_all_instructions.ocr", fake_ocr)
    monkeypatch.setattr("apparser.instructions.utils._get_all_instructions.speak", fake_speak)
    monkeypatch.setattr("apparser.instructions.utils._get_all_instructions.ui", fake_ui)

    result = _get_all_instructions()

    assert MouseClick in result
    assert custom_instruction in result
    assert BaseInstruction not in result
