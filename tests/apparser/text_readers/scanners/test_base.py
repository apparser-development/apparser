from __future__ import annotations

import pytest

from apparser.text_readers.scanners import BaseTextScanner


def test_base_text_scanner_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseTextScanner()
