from __future__ import annotations

from typing import Any

import pytest

from apparser.exceptions.debug import DebugException


def test_debug_exception_accepts_string() -> None:
    error = DebugException("message")

    assert isinstance(error, Exception)


@pytest.mark.parametrize("message", [1, None, object()])
def test_debug_exception_rejects_invalid_message_type(message: Any) -> None:
    with pytest.raises(TypeError):
        DebugException(message)
