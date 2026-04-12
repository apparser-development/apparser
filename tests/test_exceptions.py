"""Tests for project exceptions."""

import pytest

from apparser.exceptions import (
    DebugException,
    TextNotFoundException,
    WindowActionWithDesktopException,
)


@pytest.mark.parametrize(
    ("min_similarity", "error", "message"),
    [
        ("0.5", TypeError, "min_similarity must be float"),
        (-0.1, ValueError, "min_similarity must be between 0 and 1"),
        (1.1, ValueError, "min_similarity must be between 0 and 1"),
    ],
)
def test_text_not_found_exception_validation(min_similarity, error, message):
    with pytest.raises(error, match=message):
        TextNotFoundException(min_similarity)


def test_text_not_found_exception_message():
    message = "No text with similarity greater than or equal to 0.5 was found."

    assert str(TextNotFoundException(0.5)) == message


def test_window_action_with_desktop_exception_message():
    message = "You cannot treat the DesktopUi class as a window."

    assert str(WindowActionWithDesktopException()) == message


def test_debug_exception_validation():
    with pytest.raises(TypeError, match="message must be a string"):
        DebugException(1)


def test_debug_exception_message():
    assert str(DebugException("boom")) == "boom"
