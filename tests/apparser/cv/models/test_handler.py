from __future__ import annotations

from apparser.cv.events import Detected
from apparser.cv.models.handler import CvHandler


def test_cv_handler_stores_configuration() -> None:
    def callback() -> None:
        return None

    handler = CvHandler(Detected, callback, "button")

    assert handler.event is Detected
    assert handler.function is callback
    assert handler.class_name == "button"
