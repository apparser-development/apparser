from __future__ import annotations

import pytest

from apparser.movers.base import BaseMover


def test_base_mover_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseMover()
