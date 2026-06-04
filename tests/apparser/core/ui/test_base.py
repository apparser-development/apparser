from __future__ import annotations

import pytest

from apparser.core.ui.base import BaseUi


def test_base_ui_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseUi()
