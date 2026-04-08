from types import SimpleNamespace

import numpy
import pytest
from PIL import Image
from appwindows.geometry import Point, Size

import apparser.core.app as app_module
import apparser.core.ui.desktop as desktop_module
import apparser.core.ui.window as window_module
from apparser.core.app import App
from apparser.core.ui.coordinates import CoordinatesUi
from apparser.core.ui.desktop import DesktopUi
from apparser.core.ui.window import WindowUi
from apparser.exceptions import TextNotFoundException, WindowActionWithDesktopException
from apparser.geometry import RelativelyPoint, distance
from apparser.key_codes import Alt, Control, Delete, Enter, KeyboardKeyCode, LeftClick, RightClick


class DummyUi:
    def point_to_global(self, coordinates):
        return coordinates

    def point_to_local(self, coordinates):
        return coordinates

    def get_screenshot(self):
        return numpy.zeros((1, 1))

    @property
    def window(self):
        return None


def test_distance_validation_and_value():
    with pytest.raises(TypeError, match='First Point must be of type Point'):
        distance('first', Point(0, 0))

    with pytest.raises(TypeError, match='Second Point must be of type Point'):
        distance(Point(0, 0), 'second')

    assert distance(Point(1, 2), Point(4, 8)) == 9


@pytest.mark.parametrize(('x_percent', 'y_percent', 'error', 'message'), [
    ('1', 0, TypeError, 'x_percent must be number'),
    (0, '1', TypeError, 'y_percent must be number'),
    (-2, 0, ValueError, 'x must be between -1 and 1'),
    (0, 2, ValueError, 'y must be between -1 and 1'),
])
def test_relatively_point_validation(x_percent, y_percent, error, message):
    with pytest.raises(error, match=message):
        RelativelyPoint(x_percent, y_percent)


def test_relatively_point_properties():
    point = RelativelyPoint(0.25, -0.5)

    assert point.x == 0.25
    assert point.y == -0.5


@pytest.mark.parametrize(('min_similarity', 'error', 'message'), [
    ('0.5', TypeError, 'min_similarity must be float'),
    (-0.1, ValueError, 'min_similarity must be between 0 and 1'),
    (1.1, ValueError, 'min_similarity must be between 0 and 1'),
])
def test_text_not_found_exception_validation(min_similarity, error, message):
    with pytest.raises(error, match=message):
        TextNotFoundException(min_similarity)


def test_text_not_found_exception_message():
    assert str(TextNotFoundException(0.5)) == 'No text with similarity greater than or equal to 0.5 was found.'


def test_window_action_with_desktop_exception_message():
    assert str(WindowActionWithDesktopException()) == 'You cannot treat the DesktopUi class as a window.'


def test_keyboard_and_mouse_key_codes():
    assert str(KeyboardKeyCode('a')) == 'a'
    assert str(Enter()) == 'enter'
    assert str(Control()) == 'ctrl'
    assert str(Alt()) == 'alt'
    assert str(Delete()) == 'del'
    assert str(RightClick()) == 'RIGHT'
    assert str(LeftClick()) == 'LEFT'


@pytest.mark.parametrize(('path_to_exe', 'window_title', 'window_size', 'timeout', 'error', 'message'), [
    (1, 'title', Size(1, 1), 1, TypeError, 'path_to_exe must be a string'),
    ('app.exe', 1, Size(1, 1), 1, TypeError, 'window_title must be a string'),
    ('app.exe', 'title', 'size', 1, TypeError, 'window_size must be a Size'),
    ('app.exe', 'title', Size(1, 1), '1', TypeError, 'timeout must be a number'),
])
def test_app_init_validation(monkeypatch, path_to_exe, window_title, window_size, timeout, error, message):
    monkeypatch.setattr(app_module.App, 'start_app', lambda self: None)

    with pytest.raises(error, match=message):
        App(path_to_exe, window_title, window_size, timeout)


def test_app_start_and_stop(monkeypatch):
    popen_calls = []
    sleep_calls = []
    resize_calls = []
    close_calls = []
    kill_calls = []
    windows = []

    class FakeProcess:
        def kill(self):
            kill_calls.append(True)

    class FakeWindow:
        def resize(self, size):
            resize_calls.append(size)

        def close(self):
            close_calls.append(True)

    class FakeWindowUi:
        def __init__(self, window):
            windows.append(window)
            self.window = window

    class FakeFinder:
        def get_window_by_title(self, title):
            assert title == 'window'
            return FakeWindow()

    monkeypatch.setattr(app_module.subprocess, 'Popen', lambda args: popen_calls.append(args) or FakeProcess())
    monkeypatch.setattr(app_module.time, 'sleep', lambda timeout: sleep_calls.append(timeout))
    monkeypatch.setattr(app_module, 'get_finder', lambda: FakeFinder())
    monkeypatch.setattr(app_module, 'WindowUi', FakeWindowUi)

    app = App('app.exe', 'window', Size(100, 200), 2)
    app.stop_app()

    assert popen_calls == [['app.exe']]
    assert sleep_calls == [2]
    assert isinstance(app.ui, FakeWindowUi)
    assert len(windows) == 1
    assert resize_calls == [Size(100, 200)]
    assert close_calls == [True]
    assert kill_calls == [True]


def test_coordinates_ui_methods_raise_not_implemented():
    ui = CoordinatesUi(DummyUi())

    with pytest.raises(NotImplementedError):
        ui.point_to_global(Point(1, 2))

    with pytest.raises(NotImplementedError):
        ui.point_to_local(Point(1, 2))

    with pytest.raises(NotImplementedError):
        ui.get_screenshot()

    with pytest.raises(NotImplementedError):
        _ = ui.window


def test_desktop_ui_methods(monkeypatch):
    image = Image.new('RGB', (2, 2), color='white')
    monkeypatch.setattr(desktop_module, 'get_monitors', lambda: [SimpleNamespace(width=200, height=100)])
    monkeypatch.setattr(desktop_module.ImageGrab, 'grab', lambda: image)

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
        ui.point_to_global('coordinates')


def test_window_ui_validation_and_methods(monkeypatch):
    screenshot = numpy.array([[1, 2], [3, 4]])

    class FakeWindow:
        def get_points(self):
            return SimpleNamespace(left_top=Point(10, 20))

        def get_size(self):
            return Size(200, 100)

        def get_screenshot(self):
            return screenshot

    monkeypatch.setattr(window_module, 'Window', FakeWindow)

    with pytest.raises(TypeError, match='window must be Window'):
        WindowUi(object())

    window = FakeWindow()
    ui = WindowUi(window)

    assert ui.point_to_global(Point(1, 2)) == Point(11, 22)
    assert ui.point_to_global(RelativelyPoint(0.5, 0.25)) == Point(110, 45)
    assert ui.point_to_local(Point(15, 28)) == Point(5, 8)
    assert numpy.array_equal(ui.get_screenshot(), screenshot)
    assert ui.window is window

    with pytest.raises(NotImplementedError):
        ui.point_to_global('coordinates')
