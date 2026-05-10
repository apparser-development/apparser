from __future__ import annotations

import numpy
import pytest
from appwindows.geometry import Point, Size

from apparser.core.ui.window import WindowUi
from apparser.geometry import RelativelyPoint
from tests.utils import FakeWindow


def test_window_ui_rejects_invalid_window_type() -> None:
    with pytest.raises(TypeError):
        WindowUi(object())


def test_window_ui_converts_points(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("apparser.core.ui.window.Window", FakeWindow)
    window = FakeWindow(left_top=Point(10, 20), size=Size(50, 80))
    ui = WindowUi(window)

    assert ui.point_to_global(Point(1, 2)) == Point(11, 22)
    assert ui.point_to_global(RelativelyPoint(0.5, 0.25)) == Point(35, 40)
    assert ui.point_to_local(Point(11, 22)) == Point(1, 2)


def test_window_ui_returns_window_screenshot(monkeypatch: pytest.MonkeyPatch) -> None:
    screenshot = numpy.ones((2, 2, 3), dtype=numpy.uint8)
    monkeypatch.setattr("apparser.core.ui.window.Window", FakeWindow)
    window = FakeWindow(screenshot=screenshot)
    ui = WindowUi(window)

    assert numpy.array_equal(ui.get_screenshot(), screenshot)
    assert ui.window is window
