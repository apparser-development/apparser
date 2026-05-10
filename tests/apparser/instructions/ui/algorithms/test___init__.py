from __future__ import annotations

from apparser.instructions.ui import algorithms


def test_instruction_ui_algorithms_exports_expected_symbols() -> None:
    assert set(algorithms.__all__) == {
        "BaseAlgorithm",
        "Algorithm",
        "IdsAlgorithm",
        "NamesAlgorithm",
        "SpeakAlgorithm",
        "OCRAlgorithm",
        "UniqueAlgorithm",
    }
