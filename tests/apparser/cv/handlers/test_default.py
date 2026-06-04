import pytest

from apparser.cv.events import CvEvent, Detected, Moved
from apparser.cv.handlers.default import DefaultHandlers, _form_args
from apparser.cv.models import CvAllData, CvBox, CvChangeData
from tests.utils import FakeUi


def test_form_args_matches_by_annotation_type() -> None:
    ui = FakeUi()
    box = CvBox("button", 1, 2, 3, 4, 5, ui)
    changed_data = CvChangeData(Detected, box, box)
    cv_data = CvAllData([box])

    def callback(data: CvAllData, ui_arg: FakeUi, change: CvChangeData) -> None:
        return None

    result = _form_args(callback, cv_data, ui, changed_data)

    assert result == {
        "data": cv_data,
        "ui_arg": ui,
        "change": changed_data,
    }


def test_register_handler_rejects_base_event() -> None:
    handlers = DefaultHandlers()

    with pytest.raises(TypeError):
        handlers.register_handler(CvEvent)


def test_default_handlers_calls_matching_handler() -> None:
    handlers = DefaultHandlers()
    ui = FakeUi()
    box = CvBox("button", 1, 2, 3, 4, 5, ui)
    changed_data = CvChangeData(Detected, box, box)
    cv_data = CvAllData([box])
    received: list[tuple[CvChangeData, CvAllData, FakeUi]] = []

    @handlers.register_handler(Detected, class_name="button")
    def callback(change: CvChangeData, data: CvAllData, ui_arg: FakeUi) -> None:
        received.append((change, data, ui_arg))

    handlers.call(Detected, changed_data, cv_data, ui)

    assert received == [(changed_data, cv_data, ui)]


def test_default_handlers_skips_non_matching_handlers() -> None:
    handlers = DefaultHandlers()
    ui = FakeUi()
    box = CvBox("button", 1, 2, 3, 4, 5, ui)
    changed_data = CvChangeData(Detected, box, box)
    called = False

    @handlers.register_handler(Moved, class_name="other")
    def callback(change: CvChangeData) -> None:
        nonlocal called
        called = True

    handlers.call(Detected, changed_data, CvAllData([box]), ui)

    assert called is False
