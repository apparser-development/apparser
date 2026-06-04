from __future__ import annotations

import pytest

from apparser.cv.events.base import CvEvent


def test_cv_event_is_abstract() -> None:
    with pytest.raises(TypeError):
        CvEvent()
