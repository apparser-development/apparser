from __future__ import annotations

import pytest

from apparser.instructions.ui.algorithms.ocr import OCRAlgorithm
from tests.utils import FakeDebugger, FakeOcrInstruction, FakeTextReader, FakeUi


def test_ocr_algorithm_rejects_default_none_debugger() -> None:
    with pytest.raises(TypeError):
        OCRAlgorithm([])


def test_ocr_algorithm_rejects_invalid_text_reader() -> None:
    with pytest.raises(TypeError):
        OCRAlgorithm([], text_reader=object(), debugger=False)


def test_ocr_algorithm_creates_default_text_reader() -> None:
    algorithm = OCRAlgorithm([], debugger=False)

    assert algorithm.instructions == []


def test_ocr_algorithm_performs_instructions(monkeypatch: pytest.MonkeyPatch) -> None:
    instruction = FakeOcrInstruction(2000)
    reader = FakeTextReader()
    ui = FakeUi()
    algorithm = OCRAlgorithm([instruction], text_reader=reader, debugger=False)

    algorithm.perform(ui)

    assert ui.window.to_foreground_calls == 1
    assert instruction.calls == [{"args": (ui, reader), "kwargs": {}}]


def test_ocr_algorithm_uses_debugger() -> None:
    debugger = FakeDebugger(call_inner=False)
    instruction = FakeOcrInstruction(2000)
    reader = FakeTextReader()
    algorithm = OCRAlgorithm([instruction], text_reader=reader, debugger=debugger)

    algorithm.perform(FakeUi())

    assert debugger.clear_calls == 1
    assert debugger.try_calls[0]["instruction"] is instruction


def test_ocr_algorithm_rejects_invalid_instruction_on_perform() -> None:
    algorithm = OCRAlgorithm([object()], text_reader=FakeTextReader(), debugger=False)

    with pytest.raises(TypeError):
        algorithm.perform(FakeUi())


def test_ocr_algorithm_add_instruction_validates_type() -> None:
    algorithm = OCRAlgorithm([], text_reader=FakeTextReader(), debugger=False)

    with pytest.raises(TypeError):
        algorithm.add_instruction(object())


def test_ocr_algorithm_add_instruction_appends_instruction() -> None:
    algorithm = OCRAlgorithm([], text_reader=FakeTextReader(), debugger=False)
    instruction = FakeOcrInstruction(2000)

    algorithm.add_instruction(instruction)

    assert algorithm.instructions == [instruction]
