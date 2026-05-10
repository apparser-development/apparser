from __future__ import annotations

from apparser.instructions import speak


def test_instruction_speak_exports_expected_symbols() -> None:
    assert set(speak.__all__) == {"SpeakInstruction", "PlayTextAudio", "SayTextAudio"}
