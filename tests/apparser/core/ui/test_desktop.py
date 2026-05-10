from __future__ import annotations

import numpy
import pytest
from PIL import Image
from appwindows.geometry import Point

from apparser.core.ui.desktop import DesktopUi
from apparser.exceptions import WindowActionWithDesktopException
from apparser.geometry import RelativelyPoint
from tests.utils import screeninfo_stub


def test_desktop_ui_converts_points(monkeypatch: pytest.MonkeyPatch) -> None:
    screeninfo_stub.monitors = [
        type("Monitor", (), {"width": 200, "height": 100})(),
    ]
    ui = DesktopUi(display_id=0)

    assert ui.point_to_global(Point(1, 2)) == Point(1, 2)
    assert ui.point_to_global(RelativelyPoint(0.5, 0.25)) == Point(100, 25)
    assert ui.point_to_local(Point(7, 8)) == Point(7, 8)


def test_desktop_ui_returns_numpy_screenshot(monkeypatch: pytest.MonkeyPatch) -> None:
    image = Image.fromarray(numpy.ones((2, 2, 3), dtype=numpy.uint8))
    monkeypatch.setattr("apparser.core.ui.desktop.ImageGrab.grab", lambda: image)
    ui = DesktopUi()

    result = ui.get_screenshot()

    assert isinstance(result, numpy.ndarray)
    assert result.shape == (2, 2, 3)


def test_desktop_ui_has_no_window() -> None:
    ui = DesktopUi()

    with pytest.raises(WindowActionWithDesktopException):
        _ = ui.window
