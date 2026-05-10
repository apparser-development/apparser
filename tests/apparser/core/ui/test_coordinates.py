from __future__ import annotations

import numpy
import pytest
from PIL import Image
from appwindows.geometry import Point, Size

from apparser.core.ui.coordinates import CoordinatesUi
from apparser.geometry import RelativelyPoint
from tests.utils import FakeUi, FakeWindow


def test_coordinates_ui_validates_arguments() -> None:
    with pytest.raises(TypeError):
        CoordinatesUi(object(), Point(0, 0), Size(1, 1))

    with pytest.raises(TypeError):
        CoordinatesUi(FakeUi(), object(), Size(1, 1))

    with pytest.raises(TypeError):
        CoordinatesUi(FakeUi(), Point(0, 0), object())


def test_coordinates_ui_converts_points() -> None:
    parent_ui = FakeUi(offset=Point(10, 20), relative_size=Size(100, 100))
    ui = CoordinatesUi(parent_ui, Point(5, 6), Size(40, 80))

    assert ui.point_to_global(Point(1, 2)) == Point(16, 28)
    assert ui.point_to_global(RelativelyPoint(0.5, 0.25)) == Point(35, 46)
    assert ui.point_to_local(Point(16, 28)) == Point(1, 2)


def test_coordinates_ui_supports_relative_origin() -> None:
    parent_ui = FakeUi(offset=Point(10, 20), relative_size=Size(100, 100))
    ui = CoordinatesUi(parent_ui, RelativelyPoint(0.1, 0.2), Size(10, 10))

    assert ui.point_to_global(Point(1, 1)) == Point(21, 41)


def test_coordinates_ui_crops_numpy_screenshot() -> None:
    screenshot = numpy.arange(100, dtype=numpy.uint8).reshape(10, 10)
    parent_ui = FakeUi(screenshot=screenshot)
    ui = CoordinatesUi(parent_ui, Point(2, 3), Size(4, 2))

    result = ui.get_screenshot()

    assert numpy.array_equal(result, screenshot[3:5, 2:6])


def test_coordinates_ui_crops_pillow_screenshot() -> None:
    screenshot = Image.fromarray(numpy.arange(100, dtype=numpy.uint8).reshape(10, 10))

    class PillowUi(FakeUi):
        def get_screenshot(self) -> Image.Image:
            return screenshot

    parent_ui = PillowUi(window=FakeWindow())
    ui = CoordinatesUi(parent_ui, Point(1, 1), Size(3, 2))

    result = ui.get_screenshot()

    assert result.size == (3, 2)
    assert ui.window is parent_ui.window
