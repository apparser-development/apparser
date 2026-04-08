from types import SimpleNamespace

import numpy
import pytest
import ultralytics

from apparser.cv.events import CvEvent, Detected, Moved, Resized, UnDetected
from apparser.cv.handlers.default import DefaultHandlers, _form_args
from apparser.cv.models import CvAllData, CvBox, CvChangeData
from apparser.cv.processes.default import DefaultCvProcess
from apparser.cv.readers.yolo import YoloReader
from apparser.cv.utils.changes_checker import ChangesChecker, _is_moved, _is_resized


class FakeUi:
    def __init__(self):
        self.window = SimpleNamespace(get_screenshot=lambda: numpy.array([[1, 2], [3, 4]]))


def test_cv_event_strings():
    assert str(Detected()) == 'Detected'
    assert str(Moved()) == 'Moved'
    assert str(Resized()) == 'Resized'
    assert str(UnDetected()) == 'UnDetected'


def test_form_args_matches_only_exact_types():
    changed_data = CvChangeData(Detected, CvBox('cat', 1, 0, 0, 1, 1), CvBox('cat', 1, 0, 0, 1, 1))
    all_data = CvAllData([])
    ui = FakeUi()

    def handler(data: CvAllData, ui_arg: FakeUi, change: CvChangeData):
        return data, ui_arg, change

    assert _form_args(handler, changed_data, all_data, ui) == {
        'data': all_data,
        'ui_arg': ui,
        'change': changed_data,
    }


def test_default_handlers_register_and_call():
    calls = []
    handlers = DefaultHandlers()
    changed_data = CvChangeData(Detected, CvBox('cat', 1, 0, 0, 1, 1), CvBox('cat', 1, 0, 0, 1, 1))
    all_data = CvAllData([changed_data.box])
    ui = FakeUi()

    @handlers.register_handler(Detected)
    def on_detected(change: CvChangeData, data: CvAllData, ui_arg: FakeUi):
        calls.append(('detected', change, data, ui_arg))

    @handlers.register_handler(Detected, class_name='dog')
    def on_dog(change: CvChangeData):
        calls.append(('dog', change))

    handlers.call(Detected, changed_data, all_data, ui)

    with pytest.raises(TypeError, match='event must be a apparser.cv.events.CvEvent'):
        handlers.register_handler(CvEvent)

    assert calls == [('detected', changed_data, all_data, ui)]


def test_changes_checker_helpers():
    old_box = CvBox('cat', 1, 1, 1, 10, 10)
    moved_and_resized = CvBox('cat', 1, 2, 3, 12, 13)
    only_x_changed = CvBox('cat', 1, 2, 1, 12, 13)

    assert _is_moved(moved_and_resized, old_box) is True
    assert _is_moved(only_x_changed, old_box) is False
    assert _is_resized(moved_and_resized, old_box) is True
    assert _is_resized(CvBox('cat', 1, 2, 3, 12, 10), old_box) is False


def test_changes_checker_initial_state_raises():
    with pytest.raises(AttributeError):
        ChangesChecker().check(CvAllData([]))


def test_changes_checker_check_with_preloaded_old_data():
    checker = ChangesChecker()
    checker._ChangesChecker__old_data = CvAllData([
        CvBox('cat', 1, 0, 0, 10, 10),
        CvBox('dog', 2, 5, 5, 20, 20),
    ])
    data = CvAllData([
        CvBox('cat', 1, 1, 1, 12, 12),
        CvBox('bird', 3, 7, 8, 9, 10),
    ])

    result = checker.check(data)

    assert result == [
        CvChangeData(UnDetected, CvBox('dog', 2, 5, 5, 20, 20), CvBox('dog', 2, 5, 5, 20, 20)),
        CvChangeData(Moved, CvBox('cat', 1, 1, 1, 12, 12), CvBox('cat', 1, 0, 0, 10, 10)),
        CvChangeData(Resized, CvBox('cat', 1, 1, 1, 12, 12), CvBox('cat', 1, 0, 0, 10, 10)),
        CvChangeData(Detected, CvBox('bird', 3, 7, 8, 9, 10), CvBox('bird', 3, 7, 8, 9, 10)),
    ]


def test_yolo_reader_init_and_read():
    reader = YoloReader(model='fake.pt')
    fake_box = SimpleNamespace(
        cls=SimpleNamespace(item=lambda: 0),
        xyxy=[SimpleNamespace(tolist=lambda: [1.2, 2.4, 8.8, 12.9])],
    )
    ultralytics.last_model.model.names = {0: 'cat'}
    ultralytics.last_model.results = [SimpleNamespace(boxes=[fake_box])]
    image = numpy.array([[1, 2], [3, 4]])

    result = reader.read(image)

    assert ultralytics.last_model.kwargs == {'model': 'fake.pt'}
    assert ultralytics.last_model.calls == [image]
    assert result == CvAllData([CvBox('cat', 0, 1, 2, 7, 10)])


def test_default_cv_process_start_stop_and_include_handlers():
    change = CvChangeData(Detected, CvBox('cat', 1, 0, 0, 1, 1), CvBox('cat', 1, 0, 0, 1, 1))
    ui = FakeUi()
    reader_calls = []
    checker_calls = []
    handler_calls = []

    class FakeReader:
        def read(self, image):
            reader_calls.append(image)
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

    handler = FakeHandler()
    process.include_handlers(handler)
    process.start(ui)

    assert len(reader_calls) == 1
    assert numpy.array_equal(reader_calls[0], numpy.array([[1, 2], [3, 4]]))
    assert checker_calls == [CvAllData([change.box])]
    assert handler_calls == [(Detected, change, CvAllData([change.box]), ui)]
