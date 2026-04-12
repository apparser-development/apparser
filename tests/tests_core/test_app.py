"""Tests for the App class."""

import pytest
from appwindows.geometry import Size

import apparser.core.app as app_module
from apparser.core.app import App


@pytest.mark.parametrize(
    ("path_to_exe", "window_title", "window_size", "timeout", "error", "message"),
    [
        (1, "title", Size(1, 1), 1, TypeError, "path_to_exe must be a string"),
        ("app.exe", 1, Size(1, 1), 1, TypeError, "window_title must be a string"),
        ("app.exe", "title", "size", 1, TypeError, "window_size must be a Size"),
        ("app.exe", "title", Size(1, 1), "1", TypeError, "timeout must be a number"),
    ],
)
def test_app_init_validation(
    monkeypatch,
    path_to_exe,
    window_title,
    window_size,
    timeout,
    error,
    message,
):
    monkeypatch.setattr(app_module.App, "start_app", lambda self: None)

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
            assert title == "window"
            return FakeWindow()

    monkeypatch.setattr(
        app_module.subprocess,
        "Popen",
        lambda args: popen_calls.append(args) or FakeProcess(),
    )
    monkeypatch.setattr(app_module.time, "sleep", lambda timeout: sleep_calls.append(timeout))
    monkeypatch.setattr(app_module, "get_finder", lambda: FakeFinder())
    monkeypatch.setattr(app_module, "WindowUi", FakeWindowUi)

    app = App("app.exe", "window", Size(100, 200), 2)
    app.stop_app()

    assert popen_calls == [["app.exe"]]
    assert sleep_calls == [2]
    assert isinstance(app.ui, FakeWindowUi)
    assert len(windows) == 1
    assert resize_calls == [Size(100, 200)]
    assert close_calls == [True]
    assert kill_calls == [True]
