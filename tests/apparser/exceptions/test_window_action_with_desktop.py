from __future__ import annotations

from apparser.exceptions.window_action_with_desktop import WindowActionWithDesktopException


def test_window_action_with_desktop_exception_is_exception() -> None:
    error = WindowActionWithDesktopException()

    assert isinstance(error, Exception)
