from __future__ import annotations

import numpy
import pytest
from PIL import Image
from appwindows.geometry import Point, Size

from apparser.core.ui.window_by_display import WindowByDisplayUi
from apparser.geometry import RelativelyPoint
from tests.utils import FakeWindow


def test_window_by_display_ui_rejects_invalid_window_type() -> None:
    with pytest.raises(TypeError):
        WindowByDisplayUi(object())


def test_window_by_display_ui_converts_points(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "apparser.core.ui.window_by_display.Window",
        FakeWindow,
    )
    window = FakeWindow(left_top=Point(10, 20), size=Size(50, 80))
    ui = WindowByDisplayUi(window)

    assert ui.point_to_global(Point(1, 2)) == Point(11, 22)
    assert ui.point_to_global(RelativelyPoint(0.5, 0.25)) == Point(35, 40)
    assert ui.point_to_local(Point(11, 22)) == Point(1, 2)


def test_window_by_display_ui_returns_display_screenshot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    image = Image.fromarray(numpy.ones((2, 2, 3), dtype=numpy.uint8))
    grab_calls: list[dict[str, object]] = []

    def grab(
        bbox: tuple[int, int, int, int],
        all_screens: bool,
    ) -> Image.Image:
        grab_calls.append({"bbox": bbox, "all_screens": all_screens})
        return image

    monkeypatch.setattr(
        "apparser.core.ui.window_by_display.Window",
        FakeWindow,
    )
    monkeypatch.setattr(
        "apparser.core.ui.window_by_display.ImageGrab.grab",
        grab,
    )
    window = FakeWindow(left_top=Point(10, 20), size=Size(5, 7))
    ui = WindowByDisplayUi(window)

    result = ui.get_screenshot()

    assert isinstance(result, numpy.ndarray)
    assert result.shape == (2, 2, 3)
    assert grab_calls == [
        {"bbox": (10, 20, 15, 27), "all_screens": True},
    ]
    assert ui.window is window
