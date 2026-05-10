from __future__ import annotations

import pytest

from apparser.instructions.ui.algorithms.base import BaseAlgorithm


def test_base_algorithm_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseAlgorithm()
