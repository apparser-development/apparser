from __future__ import annotations

from typing import Any


class FakeChangesChecker:
    def __init__(self, results: list[list[Any]] | None = None) -> None:
        self.results = results or []
        self.calls: list[Any] = []

    def check(self, data: Any) -> list[Any]:
        self.calls.append(data)
        return self.results.pop(0)
