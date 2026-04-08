import pytest

from apparser.exceptions import TextNotFoundException, WindowActionWithDesktopException


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
