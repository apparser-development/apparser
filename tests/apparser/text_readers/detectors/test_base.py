from __future__ import annotations

import pytest

from apparser.text_readers.detectors import BaseTextDetector


def test_base_text_detector_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseTextDetector()
