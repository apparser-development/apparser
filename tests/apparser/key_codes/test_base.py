from __future__ import annotations

import pytest

from apparser.key_codes.base import BaseKeyCode


def test_base_key_code_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseKeyCode()
