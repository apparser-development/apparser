"""Tests for CV processes."""

from apparser.cv.events import Detected
from apparser.cv.models import CvAllData, CvChangeData
from apparser.cv.processes.default import DefaultCvProcess
from tests.utils.cv import CvUi, make_cv_box


def test_default_cv_process_start_stop_and_include_handlers():
    ui = CvUi()
    change = CvChangeData(Detected, make_cv_box(ui=ui), make_cv_box(ui=ui))
    reader_calls = []
    checker_calls = []
    handler_calls = []

    class FakeReader:
        def read(self, ui_arg):
            reader_calls.append(ui_arg)
            return CvAllData([change.box])

    class FakeChecker:
        def check(self, data):
            checker_calls.append(data)
            return [change]

    process = DefaultCvProcess(reader=FakeReader(), changes_checker=FakeChecker())

    class FakeHandler:
        def call(self, event, changed_data, cv_data, ui_arg):
            handler_calls.append((event, changed_data, cv_data, ui_arg))
            process.stop()

    process.include_handlers(FakeHandler())
    process.start(ui)

    assert reader_calls == [ui]
    assert checker_calls == [CvAllData([change.box])]
    assert handler_calls == [(Detected, change, CvAllData([change.box]), ui)]
