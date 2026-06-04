from __future__ import annotations

from typing import Any


class FakeCvHandlers:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def call(self, event: type[Any], changed_data: Any, *args: Any) -> None:
        self.calls.append(
            {
                "event": event,
                "changed_data": changed_data,
                "args": args,
            }
        )
