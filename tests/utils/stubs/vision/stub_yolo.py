from __future__ import annotations

from types import SimpleNamespace
from typing import Any


class StubYolo:
    def __init__(self, model: object) -> None:
        self.model_path = model
        self.model = SimpleNamespace(names={})
        self.track_calls: list[dict[str, Any]] = []
        self.track_result = [SimpleNamespace(boxes=[])]

    def track(self, **kwargs: Any) -> list[Any]:
        self.track_calls.append(kwargs)
        return self.track_result
