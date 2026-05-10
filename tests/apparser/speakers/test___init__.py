from __future__ import annotations

from apparser import speakers


def test_speakers_exports_expected_symbols() -> None:
    assert set(speakers.__all__) == {"BaseSpeaker", "TorchSpeaker", "ChatTTSSpeaker"}
