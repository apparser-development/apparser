from __future__ import annotations

from apparser.instructions import ocr


def test_instruction_ocr_exports_expected_symbols() -> None:
    assert set(ocr.__all__) == {
        "PrintAllText",
        "ClickOnText",
        "GetText",
        "MoveToText",
        "OCRInstruction",
        "PlotAllText",
    }
