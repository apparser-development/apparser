"""Tests for UI classes."""

from types import SimpleNamespace

import numpy
import pytest
from PIL import Image
from appwindows.geometry import Point, Size

import apparser.core.ui.desktop as desktop_module
import apparser.core.ui.window as window_module
from apparser.core.ui.base import BaseUi
from apparser.core.ui.coordinates import CoordinatesUi
from apparser.core.ui.desktop import DesktopUi
from apparser.core.ui.window import WindowUi
from apparser.exceptions import WindowActionWithDesktopException
from apparser.geometry import RelativelyPoint


class DummyUi(BaseUi):
    def __init__(self):
        self._window = SimpleNamespace(name="window")
        self._screenshot = numpy.arange(10000).reshape(100, 100)

    def point_to_global(self, coordinates):
        if isinstance(coordinates, RelativelyPoint):
            coordinates = Point(round(coordinates.x * 100), round(coordinates.y * 80))
        if not isinstance(coordinates, Point):
            raise NotImplementedError()
        return coordinates + Point(100, 200)

    def point_to_local(self, coordinates):
        if not isinstance(coordinates, Point):
            raise NotImplementedError()
        return coordinates - Point(100, 200)

    def get_screenshot(self):
        return self._screenshot

    @property
    def window(self):
        return self._window


@pytest.mark.parametrize(
    ("from_ui", "left_top_point", "size", "error", "message"),
    [
        ("ui", Point(1, 2), Size(10, 10), TypeError, "from_ui must be Ui"),
        (
            DummyUi(),
            "point",
            Size(10, 10),
            TypeError,
            "left_top_point must be Point or RelativelyPoint",
        ),
        (DummyUi(), Point(1, 2), "size", TypeError, "size must be Size"),
    ],
)
def test_coordinates_ui_validation(from_ui, left_top_point, size, error, message):
    with pytest.raises(error, match=message):
        CoordinatesUi(from_ui, left_top_point, size)


def test_coordinates_ui_methods():
    from_ui = DummyUi()
    ui = CoordinatesUi(from_ui, Point(10, 20), Size(30, 40))

    assert ui.point_to_global(Point(1, 2)) == Point(111, 222)
    assert ui.point_to_global(RelativelyPoint(0.5, 0.25)) == Point(125, 230)
    assert ui.point_to_local(Point(140, 260)) == Point(30, 40)
    assert numpy.array_equal(ui.get_screenshot(), from_ui.get_screenshot()[20:60, 10:40])
    assert ui.window is from_ui.window

    with pytest.raises(NotImplementedError):
        ui.point_to_global("coordinates")


def test_coordinates_ui_with_relative_left_top_point():
    ui = CoordinatesUi(DummyUi(), RelativelyPoint(0.1, 0.25), Size(30, 40))

    assert ui.point_to_global(Point(1, 2)) == Point(111, 222)
    assert ui.point_to_local(Point(130, 260)) == Point(20, 40)


def test_coordinates_ui_get_screenshot_for_image():
    from_ui = DummyUi()
    from_ui._screenshot = Image.fromarray(
        numpy.arange(10000, dtype=numpy.uint8).reshape(100, 100)
    )
    ui = CoordinatesUi(from_ui, Point(10, 20), Size(30, 40))

    assert numpy.array_equal(
        numpy.asarray(ui.get_screenshot()),
        numpy.asarray(from_ui.get_screenshot().crop((10, 20, 40, 60))),
    )


def test_desktop_ui_methods(monkeypatch):
    image = Image.new("RGB", (2, 2), color="white")
    monkeypatch.setattr(
        desktop_module,
        "get_monitors",
        lambda: [SimpleNamespace(width=200, height=100)],
    )
    monkeypatch.setattr(desktop_module.ImageGrab, "grab", lambda: image)

    ui = DesktopUi()

    assert ui.point_to_global(Point(3, 4)) == Point(3, 4)
    assert ui.point_to_global(RelativelyPoint(0.5, 0.25)) == Point(100, 25)
    assert ui.point_to_local(Point(5, 6)) == Point(5, 6)
    assert numpy.array_equal(ui.get_screenshot(), numpy.asarray(image))

    with pytest.raises(WindowActionWithDesktopException):
        _ = ui.window


def test_desktop_ui_point_to_global_for_unknown_type():
    ui = DesktopUi()

    with pytest.raises(NotImplementedError):
        ui.point_to_global("coordinates")


def test_window_ui_validation_and_methods(monkeypatch):
    screenshot = numpy.array([[1, 2], [3, 4]])

    class FakeWindow:
        def get_points(self):
            return SimpleNamespace(left_top=Point(10, 20))

        def get_size(self):
            return Size(200, 100)

        def get_screenshot(self):
            return screenshot

    monkeypatch.setattr(window_module, "Window", FakeWindow)

    with pytest.raises(TypeError, match="window must be Window"):
        WindowUi(object())

    window = FakeWindow()
    ui = WindowUi(window)

    assert ui.point_to_global(Point(1, 2)) == Point(11, 22)
    assert ui.point_to_global(RelativelyPoint(0.5, 0.25)) == Point(110, 45)
    assert ui.point_to_local(Point(15, 28)) == Point(5, 8)
    assert numpy.array_equal(ui.get_screenshot(), screenshot)
    assert ui.window is window

    with pytest.raises(NotImplementedError):
        ui.point_to_global("coordinates")
