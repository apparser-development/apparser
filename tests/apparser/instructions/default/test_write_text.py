from __future__ import annotations

from typing import Any

import pytest

from apparser.instructions.default.write_text import WriteText
from tests.utils import keyboard_stub


@pytest.mark.parametrize(
    ("text", "pause_time", "error_type"),
    [
        (1, 0.1, TypeError),
        ("text", "0.1", TypeError),
        ("", 0.1, ValueError),
    ],
)
def test_write_text_validates_arguments(text: Any, pause_time: Any, error_type: type[Exception]) -> None:
    with pytest.raises(error_type):
        WriteText(text, pause_time)


def test_write_text_uses_keyboard_backend() -> None:
    instruction = WriteText("hello", 0.2)

    instruction.perform()

    assert keyboard_stub.write_calls == [("hello", 0.2)]
    assert instruction.id == 4
