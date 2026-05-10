from __future__ import annotations

from types import ModuleType

from tests.utils.stubs.ml.fake_torch_hub import FakeTorchHub
from tests.utils.stubs.ml.fake_torch_model import FakeTorchModel


class TorchStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("torch")
        self.reset()

    def reset(self) -> None:
        self.device_calls: list[str] = []
        self.hub_load_calls: list[dict[str, object]] = []
        self.hub_model = FakeTorchModel()
        self.hub = FakeTorchHub(self)

    def device(self, value: str) -> str:
        self.device_calls.append(value)
        return f"device:{value}"
