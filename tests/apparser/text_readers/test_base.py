from __future__ import annotations

import pytest

from apparser.text_readers import BaseTextReader


def test_base_text_reader_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseTextReader()
