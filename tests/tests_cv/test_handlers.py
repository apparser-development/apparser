"""Tests for CV handlers."""

import pytest

from apparser.cv.events import CvEvent, Detected
from apparser.cv.handlers.default import DefaultHandlers, _form_args
from apparser.cv.models import CvAllData, CvChangeData
from tests.utils.cv import CvUi, make_cv_box


def test_form_args_matches_only_exact_types():
    ui = CvUi()
    changed_data = CvChangeData(
        Detected,
        make_cv_box(ui=ui),
        make_cv_box(ui=ui),
    )
    all_data = CvAllData([])

    def handler(data: CvAllData, ui_arg: CvUi, change: CvChangeData):
        return data, ui_arg, change

    assert _form_args(handler, changed_data, all_data, ui) == {
        "data": all_data,
        "ui_arg": ui,
        "change": changed_data,
    }


def test_default_handlers_register_and_call():
    calls = []
    handlers = DefaultHandlers()
    ui = CvUi()
    changed_data = CvChangeData(
        Detected,
        make_cv_box(ui=ui),
        make_cv_box(ui=ui),
    )
    all_data = CvAllData([changed_data.box])

    @handlers.register_handler(Detected)
    def on_detected(change: CvChangeData, data: CvAllData, ui_arg: CvUi):
        calls.append(("detected", change, data, ui_arg))

    @handlers.register_handler(Detected, class_name="dog")
    def on_dog(change: CvChangeData):
        calls.append(("dog", change))

    handlers.call(Detected, changed_data, all_data, ui)

    with pytest.raises(TypeError, match="event must be a apparser.cv.events.CvEvent"):
        handlers.register_handler(CvEvent)

    assert calls == [("detected", changed_data, all_data, ui)]
