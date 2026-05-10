from __future__ import annotations

from apparser.instructions import default


def test_instruction_default_exports_expected_symbols() -> None:
    assert set(default.__all__) == {
        "PressKey",
        "PressKeysCombination",
        "PlayAudio",
        "PlayAudioFile",
        "SayAudio",
        "SayAudioFile",
        "Sleep",
        "MouseClick",
        "WriteText",
    }
