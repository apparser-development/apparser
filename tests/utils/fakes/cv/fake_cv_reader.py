from __future__ import annotations

from typing import Any

from tests.utils.external_stubs import install_external_stubs


install_external_stubs()

from apparser.core.ui.base import BaseUi
from apparser.cv.readers.base import CvReader


class FakeCvReader(CvReader):
    def __init__(self, results: list[Any] | None = None) -> None:
        self.results = results or []
        self.calls: list[BaseUi] = []

    def read(self, ui: BaseUi) -> Any:
        self.calls.append(ui)
        return self.results.pop(0)
