from __future__ import annotations

from typing import Any

import pytest
from appwindows.geometry import Size

from apparser.core.app import App
from tests.utils import FakeWindow


class FakeProcess:
    def __init__(self) -> None:
        self.kill_calls = 0

    def kill(self) -> None:
        self.kill_calls += 1


class FakeWindowUi:
    def __init__(self, window: FakeWindow) -> None:
        self.window = window


class FakeFinder:
    def __init__(self, window: FakeWindow) -> None:
        self.window = window
        self.calls: list[str] = []

    def get_window_by_title(self, title: str) -> FakeWindow:
        self.calls.append(title)
        return self.window

    def get_all_windows(self) -> list[FakeWindow]:
        return [self.window]

    def get_window_by_process_id(self, process_id: int) -> FakeWindow:
        return self.window


@pytest.mark.parametrize(
    ("path_to_exe", "window_title", "window_size", "timeout"),
    [
        (1, "title", Size(1, 1), 1),
        ("path", 2, Size(1, 1), 1),
        ("path", "title", object(), 1),
        ("path", "title", Size(1, 1), "1"),
    ],
)
def test_app_validates_init_arguments(
    path_to_exe: Any,
    window_title: Any,
    window_size: Any,
    timeout: Any,
) -> None:
    with pytest.raises(TypeError):
        App(path_to_exe, window_title, window_size, timeout)


def test_app_starts_and_stops(monkeypatch: pytest.MonkeyPatch) -> None:
    process = FakeProcess()
    window = FakeWindow()
    finder = FakeFinder(window)
    sleep_calls: list[float] = []

    monkeypatch.setattr("apparser.core.app.get_finder", lambda: finder)
    monkeypatch.setattr("apparser.core.app.subprocess.Popen", lambda args: process)
    monkeypatch.setattr("apparser.core.app.time.sleep", lambda value: sleep_calls.append(value))
    monkeypatch.setattr("apparser.core.app.WindowUi", FakeWindowUi)

    app = App("app.exe", timeout=0.2)

    assert sleep_calls == [0.2]

    app.stop_app()

    assert app.ui.window.close_calls == 1
    assert process.kill_calls == 1
