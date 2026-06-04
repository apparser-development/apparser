from __future__ import annotations

from apparser.cv.events import Detected
from apparser.cv.models import CvAllData, CvBox, CvChangeData
from apparser.cv.processes.default import DefaultCvProcess
from tests.utils import FakeChangesChecker, FakeCvHandlers, FakeCvReader, FakeUi


def test_default_cv_process_starts_and_dispatches_changes() -> None:
    ui = FakeUi()
    box = CvBox("button", 1, 2, 3, 4, 5, ui)
    cv_data = CvAllData([box])
    changed_data = CvChangeData(Detected, box, box)
    reader = FakeCvReader(results=[cv_data])
    checker = FakeChangesChecker(results=[[changed_data]])
    process = DefaultCvProcess(reader, changes_checker=checker)
    handler = FakeCvHandlers()

    def stop_after_call(event: type[Detected], change: CvChangeData, *args: object) -> None:
        handler.calls.append(
            {
                "event": event,
                "changed_data": change,
                "args": args,
            }
        )
        process.stop()

    handler.call = stop_after_call
    process.include_handlers(handler)

    process.start(ui)

    assert reader.calls == [ui]
    assert checker.calls == [cv_data]
    assert handler.calls[0]["event"] is Detected
    assert handler.calls[0]["changed_data"] == changed_data


def test_default_cv_process_includes_multiple_handlers() -> None:
    ui = FakeUi()
    box = CvBox("button", 1, 2, 3, 4, 5, ui)
    cv_data = CvAllData([box])
    changed_data = CvChangeData(Detected, box, box)
    reader = FakeCvReader(results=[cv_data])
    checker = FakeChangesChecker(results=[[changed_data]])
    process = DefaultCvProcess(reader, changes_checker=checker)
    first_handler = FakeCvHandlers()
    second_handler = FakeCvHandlers()

    def stop_after_second_handler(event: type[Detected], change: CvChangeData, *args: object) -> None:
        second_handler.calls.append(
            {
                "event": event,
                "changed_data": change,
                "args": args,
            }
        )
        process.stop()

    first_handler.call = lambda event, change, *args: first_handler.calls.append(
        {
            "event": event,
            "changed_data": change,
            "args": args,
        }
    )
    second_handler.call = stop_after_second_handler
    process.include_handlers(first_handler)
    process.include_handlers(second_handler)

    process.start(ui)

    assert len(first_handler.calls) == 1
    assert len(second_handler.calls) == 1
