from __future__ import annotations

from typing import Any

from tests.utils.stubs.ml.fake_torch_tensor import FakeTorchTensor


class FakeTorchModel:
    def __init__(self) -> None:
        self.to_calls: list[Any] = []
        self.apply_tts_calls: list[dict[str, Any]] = []
        self.result = FakeTorchTensor([])

    def to(self, device: Any) -> None:
        self.to_calls.append(device)

    def apply_tts(self, **kwargs: Any) -> FakeTorchTensor:
        self.apply_tts_calls.append(kwargs)
        return self.result
