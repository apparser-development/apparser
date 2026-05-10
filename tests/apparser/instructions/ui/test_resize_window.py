from __future__ import annotations

import pytest
from appwindows.geometry import Size

from apparser.instructions.ui.resize_window import WindowResize
from tests.utils import FakeUi


def test_window_resize_rejects_invalid_size() -> None:
    with pytest.raises(TypeError):
        WindowResize(object())


def test_window_resize_resizes_window() -> None:
    ui = FakeUi()
    instruction = WindowResize(Size(20, 30))

    instruction.perform(ui)

    assert ui.window.resize_calls == [Size(20, 30)]
    assert instruction.id == 1003
