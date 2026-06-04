from __future__ import annotations

import pytest

from apparser.speakers.base import BaseSpeaker


def test_base_speaker_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseSpeaker()
