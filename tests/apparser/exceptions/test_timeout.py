from __future__ import annotations

from typing import Any

import pytest

from apparser.exceptions.timeout import TimeoutException


def test_timeout_exception_accepts_none_wait_time() -> None:
    error = TimeoutException()

    assert str(error) == "Timeout error"


def test_timeout_exception_accepts_valid_wait_time() -> None:
    error = TimeoutException(1.5)

    assert str(error) == "Timeout error. The wait lasted more than 1.5 seconds."


@pytest.mark.parametrize("wait_time", ["1", object()])
def test_timeout_exception_rejects_invalid_wait_time_type(
    wait_time: Any,
) -> None:
    with pytest.raises(TypeError):
        TimeoutException(wait_time)


def test_timeout_exception_rejects_negative_wait_time() -> None:
    with pytest.raises(ValueError):
        TimeoutException(-1)
