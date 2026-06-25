from __future__ import annotations

from typing import Any

import pytest

from apparser.exceptions.text_not_found import TextNotFoundException


@pytest.mark.parametrize("value", [0, 0.5, 1])
def test_text_not_found_accepts_valid_similarity(value: float | int) -> None:
    error = TextNotFoundException(value)

    assert isinstance(error, Exception)


@pytest.mark.parametrize("value", ["0.5", None, object()])
def test_text_not_found_rejects_invalid_similarity_type(value: Any) -> None:
    with pytest.raises(TypeError):
        TextNotFoundException(value)


@pytest.mark.parametrize("value", [-0.1, 1.1])
def test_text_not_found_rejects_out_of_range_similarity(value: float) -> None:
    with pytest.raises(ValueError):
        TextNotFoundException(float(value))
